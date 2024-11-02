#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <stdio.h>

int main(int argc, char** argv) {
    // Load image
    cv::Mat src = cv::imread("cir2.jpg", cv::IMREAD_COLOR);
    if(src.empty()) {
        printf("Could not open or find the image!\n");
        return -1;
    }

    // Convert to grayscale
    cv::Mat gray;
    cv::cvtColor(src, gray, cv::COLOR_BGR2GRAY);

    // Blur the image to reduce noise
    cv::GaussianBlur(gray, gray, cv::Size(9, 9), 2, 2);

    // Apply Hough Circle Transform
    std::vector<cv::Vec3f> circles;
    cv::HoughCircles(
        gray, circles, cv::HOUGH_GRADIENT, 1, gray.rows/8, 200, 100, 0, 0
    );

    // Draw circles on the original image
    for(size_t i = 0; i < circles.size(); i++) {
        cv::Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
        int radius = cvRound(circles[i][2]);
        // Draw the circle center
        cv::circle(src, center, 3, cv::Scalar(0, 255, 0), -1, 8, 0);
        // Draw the circle outline
        cv::circle(src, center, radius, cv::Scalar(255, 0, 0), 3, 8, 0);
    }

    // Display the result
    cv::namedWindow("Detected Circles", cv::WINDOW_AUTOSIZE);
    cv::imshow("Detected Circles", src);
    cv::waitKey(0);
    return 0;
}

