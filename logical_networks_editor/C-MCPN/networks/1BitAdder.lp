%% Network Structure
%% Neurons:
% neuron(type, unique_id)
neuron("INPUT", "INPUT_2").
neuron("INPUT", "INPUT_3").
neuron("XOR", "XOR_1").
neuron("AND", "AND_1").
neuron("XOR", "XOR_2").
neuron("AND", "AND_2").
neuron("OR", "OR_1").
neuron("OUTPUT", "OUTPUT_1").
neuron("OUTPUT", "Carry_Out").
neuron("INPUT", "Carry_In").


%% Edges:
% edge(source_id, target_id)
edge("INPUT_2", "XOR_1").
edge("INPUT_2", "AND_1").
edge("INPUT_3", "XOR_1").
edge("INPUT_3", "AND_1").
edge("XOR_1", "XOR_2").
edge("Carry_In", "XOR_2").
edge("XOR_1", "AND_2").
edge("Carry_In", "AND_2").
edge("AND_1", "OR_1").
edge("AND_2", "OR_1").
edge("XOR_2", "OUTPUT_1").
edge("OR_1", "Carry_Out").


%% Cardinality constraints:
% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.
{ edge(src, "XOR_1") : neuron("XOR", "XOR_1") } 2.
{ edge(src, "AND_1") : neuron("AND", "AND_1") } 2.
{ edge(src, "XOR_2") : neuron("XOR", "XOR_2") } 2.
{ edge(src, "AND_2") : neuron("AND", "AND_2") } 2.
{ edge(src, "OR_1") : neuron("OR", "OR_1") } 2.
{ edge(src, "OUTPUT_1") : neuron("OUTPUT", "OUTPUT_1") } 1.
{ edge(src, "Carry_Out") : neuron("OUTPUT", "Carry_Out") } 1.


%% Values:
% val(neuron_id, value).
