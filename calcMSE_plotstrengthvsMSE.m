% Full script to define brain region, calculate the MSE for B1+ field data from .mat files,
% and plot B1 field strength versus homogeneity (MSE).

%% File Names 
file_names = {'B1_field_15cm_antenna.mat', '45cmDipoleB1field.mat'};  

%% Initialize
MSE_values = zeros(1, length(file_names));
B1_strength_values = zeros(1, length(file_names));  % To store B1 field strength

% Define the boundaries of the brain region (in physical units, e.g., cm)
x_min = -10;  % Min X-coordinate of the brain region
x_max = 10;   % Max X-coordinate of the brain region
y_min = -15;  % Min Y-coordinate of the brain region
y_max = 15;   % Max Y-coordinate of the brain region
z_min = -10;   % Min Z-coordinate of the brain region
z_max = 10;   % Max Z-coordinate of the brain region

%% Loop Over Each File to Calculate MSE and Apply Brain Region Mask
for i = 1:length(file_names)
    % Load and normalize data for the current file
    [Axis0_new, Axis1_new, Axis2_new, B1_normalized] = load_and_normalize(file_names{i});
    
    % Mask the B1 field data to the brain region
    x_indices = find(Axis0_new >= x_min & Axis0_new <= x_max);
    y_indices = find(Axis1_new >= y_min & Axis1_new <= y_max);
    z_indices = find(Axis2_new >= z_min & Axis2_new <= z_max);
    
    % Mask the B1 field data
    B1_brain = B1_normalized(x_indices, y_indices, z_indices);

    % Calculate the mean B1 field strength
    B1_strength = mean(B1_brain(:));  % Mean of the B1 field strength in the brain region
    
    % Store the B1 field strength for later
    B1_strength_values(i) = B1_strength;

    % Calculate the mean value of the normalized B1+ field
    B1_mean = mean(B1_brain(:));  % Ideal field is the mean of the B1+ field
    
    % Flatten the B1 field and the ideal field for MSE calculation
    B1_flat = B1_brain(:);
    B1_ideal_flat = B1_mean * ones(size(B1_flat));  % Ideal field is the mean value
    
    % Calculate the Mean Squared Error (MSE)
    squared_diff = abs(B1_flat - B1_ideal_flat).^2;
    MSE = mean(squared_diff);  % MSE calculation across all data points

    % Store the MSE for the current file
    MSE_values(i) = MSE;
    
    % Display MSE for the current file
    disp([file_names{i}, ': MSE = ', num2str(MSE)]);
end

%% Display MSE Results
disp('Mean Squared Errors (MSE) for Each File:');
for i = 1:length(MSE_values)
    disp([file_names{i}, ': MSE = ', num2str(MSE_values(i))]);
end

%% Plot B1 Field Strength vs Homogeneity (MSE)
figure;
scatter(B1_strength_values, MSE_values, 100, 'filled', 'MarkerFaceColor', 'b');
xlabel('B1 Field Strength (Mean B1 value)');
ylabel('Homogeneity (Mean Squared Error)');
title('B1 Field Strength vs Homogeneity');
grid on;

%% Local Function for Loading and Normalizing Data
function [Axis0_new, Axis1_new, Axis2_new, B1_normalized] = load_and_normalize(file_name)
    % Load the data from the .mat file
    load(file_name);
    B1_S4L = Snapshot0(:, 1);
    
    % Compute axis midpoints
    Axis0_new = (Axis0(1:end-1) + Axis0(2:end)) / 2;
    Axis1_new = (Axis1(1:end-1) + Axis1(2:end)) / 2;
    Axis2_new = (Axis2(1:end-1) + Axis2(2:end)) / 2;

    % Reshape and normalize B1 field
    B1_S4L_abs = reshape(abs(B1_S4L), [length(Axis0_new), length(Axis1_new), length(Axis2_new)]);
    B1_normalized = B1_S4L_abs / max(B1_S4L_abs(:));  % Normalize by the maximum value
end

