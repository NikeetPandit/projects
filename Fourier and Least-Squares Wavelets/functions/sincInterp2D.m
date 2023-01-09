%--- Function performs 2D sinc interpolation 
%--- M and N are size (row, col) of original signal size
%--- Interpolates between samples band-limited
%--- Exploits separability property of Fourier Transform
%--- Extends 1D sinc interpolation


%--- Written by Nikeet Pandit

function SignalOut = sincInterp2D(SignalIn, M, N)
%% Do sinc interpolation (exploit seperability)
[m, n] = size(SignalIn); %size of decimated

%-- Across rows
[Ts, T] = ndgrid(linspace(1,n,N), 1:n); 
A1 = zeros(N, m); 
for i = 1:m
    A1(:,i) = sinc(Ts - T)*SignalIn(i,:)';
end
A1 = A1';

%-- Across columns
[Ts, T] = ndgrid(linspace(1,m,M), 1:m);
A2 = zeros(M,N); 
for i = 1:N
    A2(:,i) = sinc(Ts - T)*A1(:,i);
end
SignalOut = A2; 

end