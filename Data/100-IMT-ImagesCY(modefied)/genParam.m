clear all
listing = dir('./');
for k = 3:length(listing) % avoid using the first ones
% for k = 3:4 % avoid using the first ones
    currD = listing(k).name;
    if strcmp(currD(1:3), 'AAA') == 1 
        labelPath = strcat('./', currD, '/', currD, '.scl');
        load(labelPath, '-mat');
        
        P3Path = strcat('./', currD, '/Param_3.mat');
        P4Path = strcat('./', currD, '/Param_4.mat');
        save(P3Path,'Param_3');
        save(P4Path,'Param_4');
    end
end

