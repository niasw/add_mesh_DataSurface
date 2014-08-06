% Matlab or Octave Code to Generate this Example Data Files
% by Sun Sibai
u=linspace(0,6*pi,128);
v=linspace(0,1,32);
x=(v'*ones(size(u))).*cos(ones(size(v))'*u+3.*v'*ones(size(u)));
y=(v'*ones(size(u))).*sin(ones(size(v))'*u+3.*v'*ones(size(u)));
z=ones(size(v))'*u./5;
save('Xdata.txt','x','-ascii')
save('Ydata.txt','y','-ascii')
save('Zdata.txt','z','-ascii')