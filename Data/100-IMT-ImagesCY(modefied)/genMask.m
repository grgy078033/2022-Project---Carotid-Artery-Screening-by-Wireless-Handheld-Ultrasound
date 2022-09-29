clear all
listing = dir('./');
for k = 3:length(listing) % avoid using the first ones
% for k = 3:4 % avoid using the first ones
    currD = listing(k).name; 
    if strcmp(currD(1:3), 'AAA') == 1 
        imgPath = strcat('./', currD, '/', currD, '.CRI');
        labelPath = strcat('./', currD, '/', currD, '.scl');
        
        img=imread(imgPath); 
        load(labelPath, '-mat');
        imshow(img);
        
        [x_int, I_int]=sort(Param_3(1:2:end-1));
        y_int = (Param_4(1:2:end-1));
        y_int = y_int(I_int);
        [x_med, I_med]=sort(Param_3(2:2:end));
        y_med =(Param_4(2:2:end));
        y_med = y_med(I_med);
        x = cat(1, x_int, flip(x_med));
        y = cat(1, y_int, flip(y_med));
        roi = drawpolygon(gca,'Position',[x';y']');
        mask = createMask(roi);
        imshow(mask);
        maskPath = strcat('./', currD, '/', currD, '.png');
        imwrite(mask, maskPath);
    end
end

