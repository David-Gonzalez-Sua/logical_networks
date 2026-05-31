%% Network architecture
%% Neurons:
% nueron(type, unique_id)
nueron("OUTPUT", OUTPUT_1).


%% Edges:
% edge(source_id, target_id)


%% Values:
% val(nueron_id, value).


%% Cardinality constraints:
% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.
{ edge(src, OUTPUT_1) : neuron(type, OUTPUT_1) } 1.
