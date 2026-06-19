%% Network Structure
%% Neurons:
% neuron(type, unique_id)
neuron("XOR", "XOR_1").
neuron("AND", "AND_1").
neuron("XOR", "XOR_2").
neuron("AND", "AND_2").
neuron("OR", "OR_1").
neuron("INPUT", "INPUT_Carry").
neuron("INPUT", "A_bit_0").
neuron("INPUT", "B_bit_0").
neuron("OUTPUT", "Out_bit_0").
neuron("OUTPUT", "Out_bit_carry").


%% Edges:
% edge(source_id, target_id)
edge("A_bit_0", "XOR_1").
edge("A_bit_0", "AND_1").
edge("B_bit_0", "XOR_1").
edge("B_bit_0", "AND_1").
edge("XOR_1", "XOR_2").
edge("INPUT_Carry", "XOR_2").
edge("XOR_1", "AND_2").
edge("INPUT_Carry", "AND_2").
edge("AND_1", "OR_1").
edge("AND_2", "OR_1").
edge("XOR_2", "Out_bit_0").
edge("OR_1", "Out_bit_carry").


%% Cardinality constraints:
% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.
{ edge(src, "XOR_1") : neuron("XOR", "XOR_1") } 2.
{ edge(src, "AND_1") : neuron("AND", "AND_1") } 2.
{ edge(src, "XOR_2") : neuron("XOR", "XOR_2") } 2.
{ edge(src, "AND_2") : neuron("AND", "AND_2") } 2.
{ edge(src, "OR_1") : neuron("OR", "OR_1") } 2.
{ edge(src, "Out_bit_0") : neuron("OUTPUT", "Out_bit_0") } 1.
{ edge(src, "Out_bit_carry") : neuron("OUTPUT", "Out_bit_carry") } 1.


%% Values:
% val(neuron_id, value).
val("INPUT_Carry", 0).
val("A_bit_0", 1).
val("B_bit_0", 0).
