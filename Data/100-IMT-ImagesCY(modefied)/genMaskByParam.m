clear all
listing = dir('./');
for k = 3:length(listing) % avoid using the first ones
% for k = 3:4 % avoid using the first ones
    currD = listing(k).name; 
    if strcmp(currD(1:3), 'AAA') == 1 
        imgPath = strcat('./', currD, '/', currD, '.CRI');
        P3Path = strcat('./', currD, '/Param_3.mat');
        P4Path = strcat('./', currD, '/Param_4.mat');
        P5Path = strcat('./', currD, '/Param_5.mat');
        P6Path = strcat('./', currD, '/Param_6.mat');
        
        img=imread(imgPath); 
        load(P3Path);
        load(P4Path);
        load(P5Path);
        load(P6Path);
        imshow(img);
        
        %buttom
        [x1_int, I1_int]=sort(Param_3(1:2:end-1));
        y1_int = (Param_4(1:2:end-1));
        y1_int = y1_int(I1_int);
        [x1_med, I1_med]=sort(Param_3(2:2:end));
        y1_med =(Param_4(2:2:end));
        y1_med = y1_med(I1_med);
        x1 = cat(1, x1_int, flip(x1_med));
        y1 = cat(1, y1_int, flip(y1_med));
        roi1 = drawpolygon(gca,'Position',[x1';y1']');
        mask1 = createMask(roi1);
        
        %up
        [x2_int, I2_int]=sort(Param_5(1:2:end-1));
        y2_int = (Param_6(1:2:end-1));
        y2_int = y2_int(I2_int);
        [x2_med, I2_med]=sort(Param_5(2:2:end));
        y2_med =(Param_6(2:2:end));
        y2_med = y2_med(I2_med);
        x2 = cat(1, x2_int, flip(x2_med));
        y2 = cat(1, y2_int, flip(y2_med));
        roi2 = drawpolygon(gca,'Position',[x2';y2']');
        mask2 = createMask(roi2);
        
        mask = imadd(mask1, mask2);      
        imshow(mask);
        maskPath = strcat('./', currD, '/', currD, '.png');
        imwrite(mask, maskPath);
    end
end

