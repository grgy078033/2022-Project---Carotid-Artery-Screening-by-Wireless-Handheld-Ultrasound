clear all
listing = dir('./');
for k = 3:length(listing)
    currD = listing(k).name; 
    if strcmp(currD(1:3), 'AAA') == 1 
        % get image path
        imgPath = strcat('./', currD, '/', currD, '.CRI');
        img=imread(imgPath);
        
         % convert CRI file to PNG
%         saveAsPNG = strcat('./', currD, '/', currD, '.png');
%         imwrite(img, saveAsPNG);
%         imshow(img);
        
%         % generate Label by scl file
%         labelPath = strcat('./', currD, '/', currD, '.scl');
%         load(labelPath, '-mat');
%         [x_int, I_int]=sort(Param_3(1:2:end-1));
%         y_int = (Param_4(1:2:end-1));
%         y_int = y_int(I_int);
%         [x_med, I_med]=sort(Param_3(2:2:end));
%         y_med =(Param_4(2:2:end));
%         y_med = y_med(I_med);
%         x = cat(1, x_int, flip(x_med));
%         y = cat(1, y_int, flip(y_med));
%         roi = drawpolygon(gca,'Position',[x';y']');
%         mask = createMask(roi);
%         imshow(mask);
%         maskPath = strcat('./', currD, '/', currD, '_Label.png');
%         imwrite(mask, maskPath);
        
        % generate sobel gradient
        [f1,imgSobel] = imgradientxy(img);
        imgSobel = mat2gray(imgSobel);
        sobelPath = strcat('./', currD, '/', currD, '_sobel.png');
        imwrite(imgSobel, sobelPath);
        imshow(imgSobel);
        
        % generate Prewitt gradient
        [f2,imgPrewitt] = imgradient(img,'prewitt');
        imgPrewitt = mat2gray(imgPrewitt);
        prewittPath = strcat('./', currD, '/', currD, '_prewitt.png');
        imwrite(imgPrewitt, prewittPath);
        imshow(imgPrewitt);
        
%         % crop all png files in the current folder
%         folderPath = strcat('./', currD);
%         listingFolder = dir(folderPath);
%         for j = 3:length(listingFolder)
%             fileName = listingFolder(j).name; 
%             fullPath = strcat('./', currD, '/', fileName);
%             [filepath,name,ext] = fileparts(fullPath);
%             if strcmp(ext, '.png') == 1 
%                 toCrop = imread(fullPath);
%                 croppedImg = imcrop(toCrop,[135 90 535 465]);
%                 imshow(croppedImg);
%                 imwrite(croppedImg, fullPath);
%             end
%         end
    end
end