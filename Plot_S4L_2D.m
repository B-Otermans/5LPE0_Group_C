%% Load data in Sim4Life
files = ["sensor_0.mat" "sensor_1.mat" "sensor_2.mat" "sensor_3.mat" ...
         "sensor_4.mat" "sensor_5.mat" "sensor_6.mat" "sensor_7.mat"];
phases = [-85 -124 -185 134 95 56 -5 -46];
[total_field, Axis0, Axis1, Axis2] = loadField(files, phases);  % comment this out for faster runtime if files are loaded into workspace

plane = 'XY'; % Choose 'XY', 'XZ', or 'YZ'
slice_x = 50;
slice_y = 101;
slice_z = 198;
x_lim = [-0.1 0.1];
y_lim = [-0.13 0.1];

%% Reshape grid Sim4Life

for i = 1:length(Axis0)-1
    Axis0_new(i) = (Axis0(i) + Axis0(i+1))/2;
end

for i = 1:length(Axis1)-1
    Axis1_new(i) = (Axis1(i) + Axis1(i+1))/2;
end

for i = 1:length(Axis2)-1
    Axis2_new(i) = (Axis2(i) + Axis2(i+1))/2;
end

S4L_B1 = reshape(abs(total_field), [length(Axis0_new), length(Axis1_new), length(Axis2_new)]);
[S4L_Y, S4L_X ,S4L_Z] = meshgrid(Axis1_new, Axis0_new, Axis2_new);

%% Plot 2D Image (1D B1 Field along Z-axis)
mid_y = round(length(Axis1_new) / 2);
mid_z = round(length(Axis2_new) / 2);

B1_1D = squeeze(S4L_B1(:, mid_y, mid_z));

figure;
plot(Axis0_new, B1_1D);
xlabel('X-axis coordinates');
ylabel('B1+ Field');
title('1D B1+ Field');
grid on;

%% Plot image Sim4Life

switch plane
    case 'XZ'
        pcolor(reshape(S4L_X(:,slice_y,:), [size(S4L_B1, 1), size(S4L_B1, 3)]), ...
               reshape(S4L_Z(:,slice_y,:), [size(S4L_B1, 1), size(S4L_B1, 3)]), ...
               reshape(S4L_B1(:,slice_y,:), [size(S4L_B1, 1), size(S4L_B1, 3)]));
        xlabel('X'); ylabel('Z');
    case 'XY'
        pcolor(reshape(S4L_X(:,:,slice_z), [size(S4L_B1, 1), size(S4L_B1, 2)]), ...
               reshape(S4L_Y(:,:,slice_z), [size(S4L_B1, 1), size(S4L_B1, 2)]), ...
               reshape(S4L_B1(:,:,slice_z), [size(S4L_B1, 1), size(S4L_B1, 2)]));
        xlabel('X'); ylabel('Y');
    case 'YZ'
        pcolor(reshape(S4L_Y(slice_x,:,:), [size(S4L_B1, 2), size(S4L_B1, 3)]), ...
               reshape(S4L_Z(slice_x,:,:), [size(S4L_B1, 2), size(S4L_B1, 3)]), ...
               reshape(S4L_B1(slice_x,:,:), [size(S4L_B1, 2), size(S4L_B1, 3)]));
        xlabel('Y'); ylabel('Z');
    otherwise
        error('Invalid plane selected. Choose from ''XY'', ''XZ'', or ''YZ''.');
end

shading interp;
axis equal;
colormap(jet(256));
colorbar;
title(['Sim4Life simulation ', plane, '-section']);
%clim([0 1e-5]);
xlim(x_lim);
ylim(y_lim);


%% Load data
function [total_field, Axis0, Axis1, Axis2] = loadField(files, phases)
    load(files(1));
    total_field = Snapshot0(:, 1) * (cosd(phases(1)) + 1j*sind(phases(1)));
    for i = 2:length(files)
        load(files(i));
        total_field = total_field + Snapshot0(:, 1) * (cosd(phases(i)) + 1j*sind(phases(i)));
    end
end
