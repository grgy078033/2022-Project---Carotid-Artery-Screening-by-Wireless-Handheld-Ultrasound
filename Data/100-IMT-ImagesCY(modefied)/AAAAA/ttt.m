x0 = 1;
x1 = 4;
x2 = 6;
fx0 = log(x0);
fx1 = log(x1);
fx2 = log(x2);

l20x_x1 = [1, 0, 0]; % x^2
l20x_x2 = [0, -x1, 0]; % -x1x
l20x_x3 = [0, -x2, 0]; % -x2x
l20x_x4 = [0, 0, x1*x2]; % x1x2
l20x_y = l20x_x1 + l20x_x2 + l20x_x3 + l20x_x4; % (x-x1)*(x-x2)
l20x = l20x_y / (x0-x1) / (x0-x2); % l20x


l21x_x1 = [1, 0, 0]; % x^2
l21x_x2 = [0, -x0, 0]; % -x0x
l21x_x3 = [0, -x2, 0]; % -x2x
l21x_x4 = [0, 0, x0*x2]; % x0x2
l21x_y = l21x_x1 + l21x_x2 + l21x_x3 + l21x_x4; % (x-x0)*(x-x2)
l21x = l21x_y / (x1-x0) / (x1-x2); % l21x

l22x_x1 = [1, 0, 0]; % x^2
l22x_x2 = [0, -x0, 0]; % -x0x
l22x_x3 = [0, -x1, 0]; % -x2x
l22x_x4 = [0, 0, x0*x1]; % x0x2
l22x_y = l22x_x1 + l22x_x2 + l22x_x3 + l22x_x4; % (x-x0)*(x-x1)
l22x = l22x_y / (x2-x0) / (x2-x1); % l22x

p0 = fx0 * l20x; %fx0 * l20x
p1 = fx1 * l21x; %fx1 * l21x
p2 = fx2 * l22x; %fx2 * l22x

p = p0 + p1 + p2; % fx0*l20x+fx1*l21x+fx2*l22x