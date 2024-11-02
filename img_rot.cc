#include<iostream>
#include<opencv>

int main(){
	cv::Mat img= cv::imread("/Home/Pictures/Webcam/cap.jpg");
	
	cv::namedWindow("Input", cv::WINDOW_NORMAL);
	cv::namedWindow("Output", cv::WINDOW_NORMAL);
	cv::Mat out;

	cv::rotate(img, out, cv::ROTATE_180);
	cv::imshow("Input", img);
	cv::imshow("Output", out);

	cv::waitKey(0);
	return 0;
}
