%% Network architecture
%% Neurons:
% neuron(type, unique_id)
neuron("INPUT", "INPUT_1").
neuron("XOR", "XOR_1").
neuron("AND", "AND_1").
neuron("INPUT", "INPUT_2").
neuron("XOR", "XOR_2").
neuron("AND", "AND_2").
neuron("OR", "OR_1").
neuron("OUTPUT", "OUTPUT_1").
neuron("OUTPUT", "OUTPUT_Carry").
neuron("INPUT", "INPUT_Carry").


%% Edges:
% edge(source_id, target_id)
edge("INPUT_1", "XOR_1").
edge("INPUT_1", "AND_1").
edge("INPUT_2", "XOR_1").
edge("INPUT_2", "AND_1").
edge("INPUT_Carry", "XOR_2").
edge("INPUT_Carry", "AND_2").
edge("XOR_1", "XOR_2").
edge("XOR_1", "AND_2").
edge("AND_1", "OR_1").
edge("AND_2", "OR_1").
edge("XOR_2", "OUTPUT_1").
edge("OR_1", "OUTPUT_Carry").


%% Cardinality constraints:
% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.
{ edge(src, "XOR_1") : neuron("XOR", "XOR_1") } 2.
{ edge(src, "AND_1") : neuron("AND", "AND_1") } 2.
{ edge(src, "XOR_2") : neuron("XOR", "XOR_2") } 2.
{ edge(src, "AND_2") : neuron("AND", "AND_2") } 2.
{ edge(src, "OR_1") : neuron("OR", "OR_1") } 2.
{ edge(src, "OUTPUT_1") : neuron("OUTPUT", "OUTPUT_1") } 1.
{ edge(src, "OUTPUT_Carry") : neuron("OUTPUT", "OUTPUT_Carry") } 1.


%% Values:
% val(neuron_id, value).
val("INPUT_1", 1).
val("INPUT_2", 1).
val("INPUT_Carry", 0).
