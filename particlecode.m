clear all;
fileID = fopen('dataX.txt','r');
formatSpec = '%f';
x = fscanf(fileID,formatSpec);
fileID = fopen('dataY.txt','r');
y = fscanf(fileID,formatSpec);

scatter(x,y)