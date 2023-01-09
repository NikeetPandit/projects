%% Loading Data and Setting Variables 
clearvars
close all
addpath('data'); addpath('functions'); 
load GNSS_StateVector.mat
n = 80000; %seconds to run filter for
h = 1; %time step 
True_Measurements = GNSS_StateVector(1:n*h+1,:); %Appending extra row (first row is used for corrupted guess)

%% Corrupting True Measurements
%Adding normally distributed noise scaled by variance of Postion and Velocity 
stdPos = sqrt(1500000); stdVel = sqrt(1000); varACC = 1e-08; 

[k,j] = size(True_Measurements); Corrupted_Measurements = zeros(k,j);

rng(0,'twister'); r = normrnd(0,stdPos,[k*3,1]); %normally distributed array with mean 0 and standard deviation 
rng(1,'twister');  r1 = normrnd(0,stdVel,[k*3,1]); %normally distributed array with mean 0 and standard deviation 

for i = 1:j
    if i <= 3
        if i == 1
            Corrupted_Measurements(:,i) = True_Measurements(:,i)+ + r(1:k);
        elseif i == 2
            Corrupted_Measurements(:,i) = True_Measurements(:,i)+ + r(k+1:k*2);
        else
            Corrupted_Measurements(:,i) = True_Measurements(:,i)+ + r(k*2+1:k*3);
        end
    else
        if i == 4
            Corrupted_Measurements(:,i) = True_Measurements(:,i)+ + r1(1:k);
        elseif i == 5
            Corrupted_Measurements(:,i) = True_Measurements(:,i)+ + r1(k+1:k*2);
        else
            Corrupted_Measurements(:,i) = True_Measurements(:,i)+ + r1(k*2+1:k*3);
        end
    end
end

R = [eye(3,3)*stdPos^2 zeros(3,3); zeros(3,3) eye(3,3)*stdVel^2]; %Measurement Uncertainty 

%% Jacobian Matrix L and C
H = eye(6,6); %Jacobian of measurement function h(x) [Linear Relationship]
L = [zeros(3,3) zeros(3,3); zeros(3,3) eye(3,3)];  %Jacobian of non linear function wrt to noise vector
L = eye(6,6); 

%% Initial State Set
Xo = Corrupted_Measurements(1,:)*0.85; 
Po = R*10; %State Uncertainty (Very High)

%% Process Noise Matrix Set 
%Q = [R(1:3,1:3)*1, R(1:3,4:6)*1; R(4:6,1:3)*0.0000001 R(4:6,4:6)*0.0000001]; 
Q = [zeros(3,3) zeros(3,3); zeros(3,3) eye(3,3)*varACC];
Q = [R(1:3,1:3)*0.001 R(1:3,4:6)*0.001; zeros(3,3) eye(3,3)*0];

for i = 1:n
    
    if i == 1 %Initialization 
        Xk = Xo; 
        Pk = Po;
        to = 1; 
    end 
    
    %% Time Update (Predict State + State Covariance)

    %----------- Predict State using RK4 (Numerical Integration of System Dynamics)
    Xk_pred = rk4_prop(Xk,h);
    %----------- State Covariance Prediction 
    F = calc_sys_descrip_mat(Xk_pred(1:3));                  %Calculate System Description Matrix
    TransitionMatrix = calc_trans_mat(F,h);                  %Calculate Transition Matrix
    Pk_pred = TransitionMatrix*Pk*TransitionMatrix'+L*Q*L';  %Propagate Covariance

    %% Check Measurement 
    t = to+h; %Update Time
    Z = Corrupted_Measurements(t,:);     %State Vector Measurements from GNSS
    %% Calculate Kalman Gain 
    K = Pk_pred*H'*inv(H*Pk_pred*H'+R);     
    %% The Measurement Update (Correct)
    Xk_updated(i,:) = transpose(Xk_pred' + K*(Z'-H*Xk_pred')); 
    Pk_updated = (eye(6,6)-K*H)*Pk_pred*(eye(6,6)-K*H)' + K*R*K'; 
    
    %% And Continue...
    Xk = Xk_updated(i,:);
    Pk = Pk_updated;
    to = t;
    
  %% Saving Values for Plotting 
    Gain_Trace_Pos(i) = trace(K(1:3,1:3));
    Gain_Trace_Vel(i) = trace(K(4:6,4:6));
    True_Measurements_Saved(i,:) = True_Measurements(t,:);
    Corrupted_Measurements_Saved(i,:) = Corrupted_Measurements(t,:); 
    accel_total(i,:) = calc_acc(Corrupted_Measurements(t,1:3));   
    
    
end

% %% RSS Calculation 

j = 1:3;
k = 4:6;
clear POS_Residual_Estimate POS_Residual_Measurement VEL_Residual_Estimate VEL_Residual_Measurement
for i = 150:length(True_Measurements)-1
    comp = i-149; 
    POS_Residual_Estimate(comp) = norm(True_Measurements_Saved(i,j)-Xk_updated(i,j));
    POS_Residual_Measurement(comp) = norm(True_Measurements_Saved(i,j)-Corrupted_Measurements_Saved(i,j));
    VEL_Residual_Estimate(comp) = norm(True_Measurements_Saved(i,k)-Xk_updated(i,k));
    VEL_Residual_Measurement(comp) = norm(True_Measurements_Saved(i,k)-Corrupted_Measurements_Saved(i,k));
    if  i == length(150:length(True_Measurements)-1)
        POS_Residual_Estimate_Avg = (sum(POS_Residual_Estimate)/length(POS_Residual_Estimate));
        POS_Residual_Measurement_Avg = (sum(POS_Residual_Measurement)/length(POS_Residual_Measurement));
        VEL_Residual_Estimate_Avg = sum(VEL_Residual_Estimate)/length(VEL_Residual_Estimate);
        VEL_Residual_Measurement_Avg = sum(VEL_Residual_Measurement)/length(VEL_Residual_Measurement);
    
        disp(POS_Residual_Estimate_Avg)
        disp(POS_Residual_Measurement_Avg)
        disp(VEL_Residual_Estimate_Avg)
        disp(VEL_Residual_Measurement_Avg)
    
    end

end




% Plotting 

figure(1) %---- Plotting Norm of Position 

j = 1:3;
for i = 1:length(True_Measurements)-1
    Norm_Measurement(i) = norm(True_Measurements_Saved(i,j));
    Norm_Corrupted_Measurements(i) = norm(Corrupted_Measurements_Saved(i,j));
    Norm_Xk_Updated(i) = norm(Xk_updated(i,j)); 
end
plot(Norm_Measurement-Norm_Corrupted_Measurements,'-og'); hold on 
plot(Norm_Measurement-Norm_Xk_Updated,'-or') 
legend('Measurement Error','Estimate Error'); axis tight; grid on; grid minor 
xlabel('Time [s]'); ylabel('Position Error [m]'); 
title('Norm of Position Errors'); 

figure(2)%---- Plotting Norm of Position After Filter Stabilization 
i = 150;
plot(Norm_Measurement(i:end)-Norm_Corrupted_Measurements(i:end),'-og'); hold on 
plot(Norm_Measurement(i:end)-Norm_Xk_Updated(i:end),'-or') 
legend('Measurement Error','Estimate Error'); axis tight; grid on; grid minor 
xlabel('Time [s]'); ylabel('Position Error [m]'); 
title('Norm of Position Errors After Filter Stabilization'); 
% 
% figure(3) %---- Plotting Norm of Velocity 
% j = 4:6;
% for i = 1:length(True_Measurements)-1
%     Norm_Measurement_Vel(i) = norm(True_Measurements_Saved(i,j));
%     Norm_Corrupted_Measurements_Vel(i) = norm(Corrupted_Measurements_Saved(i,j));
%     Norm_Xk_Updated_Vel(i) = norm(Xk_updated(i,j)); 
% end
% plot(Norm_Measurement_Vel-Norm_Corrupted_Measurements_Vel,'-og'); hold on 
% plot(Norm_Measurement_Vel-Norm_Xk_Updated_Vel,'-or') 
% legend('Measurement Error','Estimate Error'); axis tight; grid on; grid minor 
% xlabel('Time [s]'); ylabel('Velocity Error [m/s]'); 
% title('Norm of Velocity Errors')
% 
% figure(4) %---- Plotting Norm of Velocity After Filter Stabilization 
% i = 150;
% plot(Norm_Measurement_Vel(i:end)-Norm_Corrupted_Measurements_Vel(i:end),'-og'); hold on 
% plot(Norm_Measurement_Vel(i:end)-Norm_Xk_Updated_Vel(i:end),'-or') 
% legend('Measurement Error','Estimate Error'); axis tight; grid on; grid minor 
% xlabel('Time [s]'); ylabel('Velocity Error [m/s]'); 
% title('Norm of Velocity Errors After Filter Stabilization'); 
% 
figure(5)
semilogx(Gain_Trace_Pos); hold on; axis tight; grid on; grid minor
semilogx(Gain_Trace_Vel); 
xlabel('Time [s]'); ylabel('Kalman Gain'); 
title('Trace of Kalman Gain: Position and Velocity States'); 
legend('Position Gain','Velocity Gain'); 
Error = True_Measurements_Saved-Corrupted_Measurements_Saved;

% figure(6)
% subplot(2,1,1); 
% j = 1;
% i = 500:600;
% plot(True_Measurements_Saved(i,j),'-og'); hold on 
% plot(Corrupted_Measurements_Saved(i,j),'-ob'); 
% plot(Xk_updated(i,j),'-or') 
% legend('True','Measurements','Estimates'); xlabel('Time'); ylabel('Position [m]')
% title('Position in X - Kalman Filter Solution'); 
% 
% 
% 


