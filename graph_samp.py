import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# Pose representation (x, y, theta)
class Vertex:
    def __init__(self, id, x, y, theta):
        self.id = id
        self.x = x
        self.y = y
        self.theta = theta  # Orientation (in radians)
    
    def to_vector(self):
        return np.array([self.x, self.y, self.theta])
    
    def update(self, delta):
        self.x += delta[0]
        self.y += delta[1]
        self.theta += delta[2]

# Edge representing a relative transformation between two vertices
class Edge:
    def __init__(self, vertex_i, vertex_j, measurement, information_matrix):
        self.vertex_i = vertex_i  # Start vertex
        self.vertex_j = vertex_j  # End vertex
        self.measurement = measurement  # Relative measurement [dx, dy, dtheta]
        self.information_matrix = information_matrix  # Information matrix (covariance inverse)

    # Calculate the error between expected and actual pose transformations
    def error(self):
        xi = self.vertex_i.to_vector()
        xj = self.vertex_j.to_vector()
        z = self.measurement
        
        # Relative transformation prediction
        delta_x = xj[0] - xi[0]
        delta_y = xj[1] - xi[1]
        delta_theta = xj[2] - xi[2]

        prediction = np.array([delta_x, delta_y, delta_theta])
        error = prediction - z
        return error

# Graph-based SLAM class
class GraphSLAM:
    def __init__(self):
        self.vertices = []
        self.edges = []

    # Add a vertex (pose)
    def add_vertex(self, vertex):
        self.vertices.append(vertex)
    
    # Add an edge (constraint)
    def add_edge(self, edge):
        self.edges.append(edge)

    # Optimize using Gauss-Newton
    def optimize(self, max_iterations=10):
        num_vertices = len(self.vertices)
        dim = 3  # State space dimension: (x, y, theta)
        
        for iteration in range(max_iterations):
            H = lil_matrix((num_vertices * dim, num_vertices * dim))
            b = np.zeros(num_vertices * dim)
            
            # Build the system of equations
            for edge in self.edges:
                i = edge.vertex_i.id
                j = edge.vertex_j.id
                error = edge.error()
                
                # Information matrix weights the error
                omega = edge.information_matrix
                
                # Jacobian matrices
                J_i = -np.eye(3)  # Jacobian for vertex i
                J_j = np.eye(3)   # Jacobian for vertex j
                
                # Update H and b
                H[3*i:3*(i+1), 3*i:3*(i+1)] += J_i.T @ omega @ J_i
                H[3*i:3*(i+1), 3*j:3*(j+1)] += J_i.T @ omega @ J_j
                H[3*j:3*(j+1), 3*i:3*(i+1)] += J_j.T @ omega @ J_i
                H[3*j:3*(j+1), 3*j:3*(j+1)] += J_j.T @ omega @ J_j
                
                b[3*i:3*(i+1)] += J_i.T @ omega @ error
                b[3*j:3*(j+1)] += J_j.T @ omega @ error

            # Fix the first pose to anchor the solution (set H[0:3, 0:3] as identity)
            H[0:3, 0:3] += np.eye(3)

            # Solve the linear system H * dx = -b
            dx = spsolve(H.tocsr(), -b)

            # Update the vertices with the solution dx
            for idx, vertex in enumerate(self.vertices):
                vertex.update(dx[3*idx:3*(idx+1)])
            
            print(f"Iteration {iteration + 1}, error norm: {np.linalg.norm(b)}")
            if np.linalg.norm(b) < 1e-5:
                break
    
    # Plot the graph
    def plot(self):
        plt.figure()
        for edge in self.edges:
            xi = edge.vertex_i.to_vector()
            xj = edge.vertex_j.to_vector()
            plt.plot([xi[0], xj[0]], [xi[1], xj[1]], 'b-')
        
        for vertex in self.vertices:
            plt.plot(vertex.x, vertex.y, 'ro')
        
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Graph SLAM')
        plt.grid()
        plt.show()

# Example of constructing and optimizing a simple graph
def main():
    slam = GraphSLAM()

    # Add vertices (poses)
    v0 = Vertex(0, 0, 0, 0)
    v1 = Vertex(1, 1, 0, 0)
    v2 = Vertex(2, 2, 1, 0)
    
    slam.add_vertex(v0)
    slam.add_vertex(v1)
    slam.add_vertex(v2)

    # Add edges (relative transformations)
    z1 = np.array([1, 0, 0])  # Relative transformation between v0 and v1
    z2 = np.array([1, 1, 0])  # Relative transformation between v1 and v2

    omega = np.eye(3)  # Information matrix (identity for simplicity)

    e1 = Edge(v0, v1, z1, omega)
    e2 = Edge(v1, v2, z2, omega)

    slam.add_edge(e1)
    slam.add_edge(e2)

    # Optimize the graph
    slam.optimize()

    # Plot the result
    slam.plot()

if __name__ == '__main__':
    main()
