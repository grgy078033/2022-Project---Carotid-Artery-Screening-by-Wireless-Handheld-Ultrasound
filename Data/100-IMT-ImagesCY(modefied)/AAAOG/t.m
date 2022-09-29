clear all
a = imread('../AAAOG/AAAOG.CRI');

filt_sobel = fspecial('sobel');
filt_prewitt = fspecial('prewitt');
outim_sobel = imfilter(double(a), filt_sobel);
outim_prewitt = imfilter(double(a), filt_prewitt);
imagesc(outim_sobel);
colormap gray;