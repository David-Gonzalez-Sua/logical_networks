%% Network architecture
%% Neurons:
% nueron(type, unique_id)
nueron("INPUT", INPUT_1).
nueron("XOR", XOR_1).
nueron("AND", AND_1).
nueron("INPUT", INPUT_2).
nueron("INPUT", INPUT_3).
nueron("XOR", XOR_2).
nueron("AND", AND_2).
nueron("OR", OR_1).
nueron("OUTPUT", OUTPUT_1).


%% Edges:
% edge(source_id, target_id)
edge(INPUT_1, XOR_1).
edge(INPUT_1, AND_1).
edge(INPUT_2, XOR_1).
edge(INPUT_2, AND_1).
edge(INPUT_3, XOR_2).
edge(INPUT_3, AND_2).
edge(XOR_1, XOR_2).
edge(XOR_1, AND_2).
edge(AND_1, OR_1).
edge(AND_2, OR_1).
edge(XOR_2, OUTPUT_1).


%% Values:
% val(node_id, value).


%% Cardinality constraints:
% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.
{ edge(src, XOR_1) : neuron(type, XOR_1) } 2.
{ edge(src, AND_1) : neuron(type, AND_1) } 2.
{ edge(src, XOR_2) : neuron(type, XOR_2) } 2.
{ edge(src, AND_2) : neuron(type, AND_2) } 2.
{ edge(src, OR_1) : neuron(type, OR_1) } 2.
{ edge(src, OUTPUT_1) : neuron(type, OUTPUT_1) } 1.
