%% function calls
files = ["sensor_0.mat" "sensor_1.mat" "sensor_2.mat" "sensor_3.mat" ...
         "sensor_4.mat" "sensor_5.mat" "sensor_6.mat" "sensor_7.mat"];
z_slices = 215:235;  % slices for which homogeneity is scored
% b1_plus_fields = initialiseFieldsMatrix(files, z_slices);  % comment this out for faster runtime if files are loaded into workspace

% alle fases 0 graden:
% start_phases = [0 0 0 0 0 0 0 0];  % cov -> 0.2512

% fases die de cirkel-hoek van de antennes in de array zijn:
% start_phases = [90 135 180 -135 -90 -45 0 45];  % cov -> 0.2374

% fases die de ellips-hoek van de antennes in de array zijn:
% start_phases = [-90 -129 -180 129 90 51 0 -51];  % cov -> 0.2107

% experimenteel succesvolle fases:
% start_phases = [-85 -124 -185 134 95 56 -5 -46];  % cov -> 0.2107
% start_phases = [-83 -126 -187 136 97 54 -7 -48];  % cov -> 0.2107

phasesOptimiser = @(phases) phasesScorer(phases, b1_plus_fields);
[optimised_phases, cofv] = fminunc(phasesOptimiser, start_phases);
disp("Best phases: "); disp(optimised_phases);
disp("Score (cov): "); disp(cofv);


%% optimiser functions
function [score] = phasesScorer(phases, fields)
    phased_fields = phaseFields(fields, phases);    
    total_field_abs = abs(sum(phased_fields, 4));
    score = cov(total_field_abs);
end


%% homogeneity qualifier functions
function cofv = cov(A)
    [S, M] = std(A, 0, "all", "omitnan");
    cofv = S/M;
end


function err = mse(A)
    At = A(~isnan(A));
    B = mean(At)*ones(size(At));
    err = immse(At, B);
end


function err = normMSE(A)
    cumulative_error = 0;
    length = 0;
    mean_value = mean(A, "all", "omitnan");
    for idx = 1:numel(A)
        val = A(idx);
        if ~isnan(val)
            error = (1 - val/mean_value)^2;
            cumulative_error = cumulative_error + error;
            length = length + 1;
        end
    end
    err = cumulative_error/length;
end


%% field functions
function phased_field = phaseFields(B1_plus_fields, phases)
    phased_field = B1_plus_fields;
    for i = 1:length(phases)
        phased_field(:,:,:, i) = phased_field(:,:,:, i) * (cosd(phases(i)) + 1j*sind(phases(i)));
    end
end


function B1_plus_fields = initialiseFieldsMatrix(files, z_slices)
    B1_plus_fields = arrayfun(@(file) loadB1Plus(file), files, "UniformOutput", false);
    B1_plus_fields = cat(4, B1_plus_fields{:});
    B1_plus_fields = double(B1_plus_fields(:,:, z_slices, :));
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


%% plot functions
function showField(fields, phases, z_index)
    phased_fields = phaseFields(fields, phases);    
    total_field_abs = abs(sum(phased_fields(:,:, z_index, :), 4));
    imshow(total_field_abs, [], Colormap=colormap('hot'));
end
