clear all
a = imread('../AAAAA/AAAAA.CRI');
%b = strel('square', 3);
%a = imopen(a, b); % opening
%a = imclose(a, b); % closing
a = im2gray(a);
%a = imnoise(a, 'gaussian',0,0.01);%對灰度圖像加入均值爲0，方差爲0.01的高斯噪聲
figure; imshow(a);
%figure; imshow(fo);
%figure; imshow(foc);

[Gmag_sobel, Gdir_sobel] = imgradientxy(a,'sobel');
[Gmag_prewitt, Gdir_prewitt] = imgradientxy(a,'prewitt');
%test1 = edge(a, 'sobel', 0.06);
%test2 = edge(a, 'prewitt', 0.06);

%figure; imshow(test1);
%figure; imshow(test2);
figure; imshow((Gdir_sobel + 4) / 8);
figure; imshow((Gdir_prewitt + 4) / 8);