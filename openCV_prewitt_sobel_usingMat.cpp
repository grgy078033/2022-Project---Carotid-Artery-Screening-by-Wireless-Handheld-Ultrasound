#include<opencv2/opencv.hpp>
using namespace cv;

Mat SuperResolution::imgsToSobel(Mat srcImage){
    cv::cvtColor(srcImage, srcImage, cv::COLOR_BGR2GRAY);   // RGB to Gray // image in opencv is RGB as default
    Mat dstImage;
    int ddepth = CV_8U;

    int ksize = 3;
    int scale = 1; // default
    int delta = 0; // default

    Sobel(srcImage, dstImage, ddepth, 0, 1, ksize, scale, delta, BORDER_DEFAULT); // y direction
    return dstImage;
}

Mat SuperResolution::imgsToPrewitt(Mat srcImage){
    cv::cvtColor(srcImage, srcImage, cv::COLOR_BGR2GRAY);   // RGB to Gray // image in opencv is RGB as default
    srcImage.convertTo(srcImage, CV_64F);

    int ddepth = -1;
    Point anchor = Point(-1, -1);
    Mat Prewitt, grad_x, grad_y;
    Mat kernelx = (Mat_<double>(3,3) << -1., -1., -1., 0., 0., 0., 1., 1., 1.);
    Mat kernely = (Mat_<double>(3,3) << -1, 0, 1, -1, 0, 1, -1, 0, 1);

    // OpenCV convolution
    cv::filter2D(srcImage, grad_x, ddepth, kernelx, anchor, cv::BORDER_CONSTANT);
    cv::filter2D(srcImage, grad_y, ddepth, kernely, anchor, cv::BORDER_CONSTANT);

    // clip grad_x & grad_y
    for(size_t i = 0; i < grad_x.rows; ++i) {
        for(size_t j = 0; j < grad_x.cols; ++j) {
            if(grad_x.ptr<uchar>(i)[j] < 0.0) grad_x.ptr<uchar>(i)[j] = 0.0;
            else if(grad_x.ptr<uchar>(i)[j] > 255.0) grad_x.ptr<uchar>(i)[j] = 255.0;
        }
    }
    for(size_t i = 0; i < grad_y.rows; ++i) {
        for(size_t j = 0; j < grad_y.cols; ++j) {
            if(grad_y.ptr<uchar>(i)[j] < 0.0) grad_y.ptr<uchar>(i)[j] = 0.0;
            else if(grad_y.ptr<uchar>(i)[j] > 255.0) grad_y.ptr<uchar>(i)[j] = 255.0;
        }
    }

    // convert to float64
    grad_x.convertTo(grad_x, CV_64F);
    grad_y.convertTo(grad_y, CV_64F);

    // generate Prewitt image && negative
    Prewitt = 1.0 - grad_x + grad_y;
    
    return Prewitt;
}