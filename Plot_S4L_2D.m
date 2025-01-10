%% Load data in Sim4Life
% B1 == 1 plot B1+ ---- B1 == 0 plot B1-
B1 = 1;

if B1 == 1
    load('sensor_0.mat');
    B1_S4L = Snapshot0(:, 1);
elseif B1 == 0
    load('B1Field.mat');
    B1_S4L = Snapshot0(:, 2);
else
    return
end

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

S4L_B1 = reshape(abs(B1_S4L), [length(Axis0_new), length(Axis1_new), length(Axis2_new)]);
[S4L_Y, S4L_X ,S4L_Z] = meshgrid(Axis1_new, Axis0_new, Axis2_new);

%% Plot 2D Image (1D B1 Field along Z-axis)
mid_y = round(length(Axis1_new) / 2);
mid_z = round(length(Axis2_new) / 2);

B1_1D = squeeze(B1_S4L_abs(:, mid_y, mid_z));

figure;
plot(Axis0_new, B1_1D);
xlabel('X-axis coordinates');
ylabel('B1+ Field');
title('1D B1+ Field');
grid on;

%% Plot image Sim4Life

plane = 'XY'; % Choose 'XY', 'XZ', or 'YZ'

switch plane
    case 'XZ'
        slice_y = 101;
        pcolor(reshape(S4L_X(:,slice_y,:), [size(S4L_B1, 1), size(S4L_B1, 3)]), ...
               reshape(S4L_Z(:,slice_y,:), [size(S4L_B1, 1), size(S4L_B1, 3)]), ...
               reshape(S4L_B1(:,slice_y,:), [size(S4L_B1, 1), size(S4L_B1, 3)]));
        xlabel('X'); ylabel('Z');
    case 'XY'
        slice_z = 198;
        pcolor(reshape(S4L_X(:,:,slice_z), [size(S4L_B1, 1), size(S4L_B1, 2)]), ...
               reshape(S4L_Y(:,:,slice_z), [size(S4L_B1, 1), size(S4L_B1, 2)]), ...
               reshape(S4L_B1(:,:,slice_z), [size(S4L_B1, 1), size(S4L_B1, 2)]));
        xlabel('X'); ylabel('Y');
    case 'YZ'
        slice_x = 50;
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
xlim([-0.4 0.4]);
ylim([-0.4 0.4]);


%% Load data
function field = loadField(files, phases)
    b1_plus_fields = initialiseFieldsMatrix(files);
    phased_fields = phaseFields(b1_plus_fields, phases);    
    field = abs(sum(phased_fields, 4));
end


function phased_field = phaseFields(B1_plus_fields, phases)
    phased_field = B1_plus_fields;
    for i = 1:length(phases)
        phased_field(:,:,:, i) = phased_field(:,:,:, i) * (cosd(phases(i)) + 1j*sind(phases(i)));
    end
end


function B1_plus_fields = initialiseFieldsMatrix(files)
    B1_plus_fields = arrayfun(@(file) loadB1Plus(file), files, "UniformOutput", false);
    B1_plus_fields = cat(4, B1_plus_fields{:});
end


function B1_plus = loadB1Plus(file_name)
    load(file_name);

    B1_plus_data = Snapshot0(:, 1);
    
    % Compute axis midpoints
    Axis0_new = (Axis0(1:end-1) + Axis0(2:end)) / 2;
    Axis1_new = (Axis1(1:end-1) + Axis1(2:end)) / 2;
    Axis2_new = (Axis2(1:end-1) + Axis2(2:end)) / 2;
    
    % Reshape B1 field
    B1_plus = reshape(B1_plus_data, [length(Axis0_new), length(Axis1_new), length(Axis2_new)]);
end