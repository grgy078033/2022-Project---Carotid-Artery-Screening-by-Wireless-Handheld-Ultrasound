%To extract the IMT area from the snakes segmented images for further image
%processing and or texture analysis. 
% a         : input image (original, normalised, despeckled) 
%out        : extracted image shown only the IMT  segmented area
%SnsakePointsfinal: adventitia and intima points from the segmentation
%algorithm 

function out=extract_imt_area(a)
%a                  : input image with plaque to be extracted
%snakePointsfinal  : adventitia snakePoints extracted from snake algo 
%snakePoints2final : intima snakePoints extracted from snake algo 
a=imread(a);

load snakePointsfinal; 
load snakePoints2final;

snakepoints=[snakePointsfinal, fliplr(snakePoints2final)];

[x, y, BW, xi, yi]=roipoly(a, snakepoints(2,:), snakepoints(1,:) );
BWoutline=bwperim(BW);
%figure, imshow(BW);
mask=~(BW&a(:,:,1));  

seg_imt=double(a).*double(BW)./255;
out=~BW+seg_imt;
figure, imshow(out);

