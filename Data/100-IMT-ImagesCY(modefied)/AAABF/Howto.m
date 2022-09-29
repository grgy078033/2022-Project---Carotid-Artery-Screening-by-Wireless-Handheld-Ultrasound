clear all
a=imread('../AAABF/AAABF.CRI');
load ('Param_3.mat');
load ('Param_4.mat');
load ('Param_5.mat');
load ('Param_6.mat');
%save('Param_5.mat', 'Param_5');
%save('Param_6.mat', 'Param_6');

figure, imshow(a);

%bottom
x1_int=Param_3(1:2:end-1);
y1_int=Param_4(1:2:end-1);
line(x1_int,y1_int,'LineWidth',1,'Color',[1 1 0],'Marker','x','MarkerEdgeColor',[1 0 0]);
intima1=[ x1_int, y1_int];

x1_med=Param_3(2:2:end);
y1_med=Param_4(2:2:end);
media1=[x1_med, y1_med];
line(x1_med,y1_med,'LineWidth',1,'Color',[1 1 0],'Marker','x','MarkerEdgeColor',[1 0 0]);
snpoints1=[intima1', fliplr(media1')];

%up
x2_int=Param_5(1:2:end-1);
y2_int=Param_6(1:2:end-1);
line(x2_int,y2_int,'LineWidth',1,'Color',[1 1 0],'Marker','x','MarkerEdgeColor',[1 0 0]);
intima2=[ x2_int, y2_int];

x2_med=Param_5(2:2:end);
y2_med=Param_6(2:2:end);
media2=[x2_med, y2_med];
line(x2_med,y2_med,'LineWidth',1,'Color',[1 1 0],'Marker','x','MarkerEdgeColor',[1 0 0]);
snpoints2=[intima2', fliplr(media2')];

save('Param_3.mat', 'Param_3');
save('Param_4.mat', 'Param_4');
save('Param_5.mat', 'Param_5');
save('Param_6.mat', 'Param_6');