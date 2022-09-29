a=imread('AAAAA.cri'); load ('AAAAA.scl', '-mat');
figure, imshow(a);
x_int=Param_3(1:2:end-1);
y_int=Param_4(1:2:end-1);
line(x_int,y_int,'LineWidth',1,'Color',[1 1 0],'Marker','x','MarkerEdgeColor',[1 0 0]);
intima=[ x_int, y_int];
x_med=Param_3(2:2:end);
y_med=Param_4(2:2:end);
media=[x_med, y_med];

line(x_med,y_med,'LineWidth',1,'Color',[1 1 0],'Marker','x','MarkerEdgeColor',[1 0 0]);
snpoints=[intima', fliplr(media')];