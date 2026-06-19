%% Network Structure
%% Neurons:
% neuron(type, unique_id)
neuron("INPUT", "INPUT_Carry").
neuron("XOR", "XOR_1").
neuron("AND", "AND_1").
neuron("XOR", "XOR_2").
neuron("AND", "AND_2").
neuron("OR", "OR_1").
neuron("XOR", "XOR_3").
neuron("AND", "AND_3").
neuron("XOR", "XOR_4").
neuron("AND", "AND_4").
neuron("OR", "OR_2").
neuron("XOR", "XOR_5").
neuron("AND", "AND_5").
neuron("XOR", "XOR_6").
neuron("AND", "AND_6").
neuron("OR", "OR_3").
neuron("XOR", "XOR_7").
neuron("AND", "AND_7").
neuron("XOR", "XOR_8").
neuron("AND", "AND_8").
neuron("OR", "OR_4").
neuron("XOR", "XOR_9").
neuron("AND", "AND_9").
neuron("XOR", "XOR_10").
neuron("AND", "AND_10").
neuron("OR", "OR_5").
neuron("XOR", "XOR_11").
neuron("AND", "AND_11").
neuron("XOR", "XOR_12").
neuron("AND", "AND_12").
neuron("OR", "OR_6").
neuron("XOR", "XOR_13").
neuron("AND", "AND_13").
neuron("XOR", "XOR_14").
neuron("AND", "AND_14").
neuron("OR", "OR_7").
neuron("XOR", "XOR_15").
neuron("AND", "AND_15").
neuron("XOR", "XOR_16").
neuron("AND", "AND_16").
neuron("OR", "OR_8").
neuron("INPUT", "A_bit_0").
neuron("OUTPUT", "Out_bit_0").
neuron("INPUT", "B_bit_0").
neuron("OUTPUT", "Out_bit_1").
neuron("OUTPUT", "Out_bit_2").
neuron("OUTPUT", "Out_bit_3").
neuron("OUTPUT", "Out_bit_4").
neuron("OUTPUT", "Out_bit_5").
neuron("OUTPUT", "Out_bit_6").
neuron("OUTPUT", "Out_bit_7").
neuron("OUTPUT", "Out_bit_carry").
neuron("INPUT", "A_bit_1").
neuron("INPUT", "A_bit_2").
neuron("INPUT", "A_bit_3").
neuron("INPUT", "A_bit_4").
neuron("INPUT", "A_bit_5").
neuron("INPUT", "A_bit_6").
neuron("INPUT", "A_bit_7").
neuron("INPUT", "B_bit_1").
neuron("INPUT", "B_bit_3").
neuron("INPUT", "B_bit_2").
neuron("INPUT", "B_bit_4").
neuron("INPUT", "B_bit_5").
neuron("INPUT", "B_bit_6").
neuron("INPUT", "B_bit_7").


%% Edges:
% edge(source_id, target_id)
edge("A_bit_0", "XOR_1").
edge("A_bit_0", "AND_1").
edge("B_bit_0", "XOR_1").
edge("B_bit_0", "AND_1").
edge("XOR_1", "XOR_2").
edge("XOR_1", "AND_2").
edge("AND_1", "OR_1").
edge("AND_2", "OR_1").
edge("XOR_2", "Out_bit_0").
edge("A_bit_1", "XOR_3").
edge("A_bit_1", "AND_3").
edge("B_bit_1", "XOR_3").
edge("B_bit_1", "AND_3").
edge("XOR_3", "XOR_4").
edge("XOR_3", "AND_4").
edge("AND_3", "OR_2").
edge("AND_4", "OR_2").
edge("XOR_4", "Out_bit_1").
edge("OR_1", "XOR_4").
edge("OR_1", "AND_4").
edge("A_bit_2", "XOR_5").
edge("A_bit_2", "AND_5").
edge("B_bit_2", "XOR_5").
edge("B_bit_2", "AND_5").
edge("XOR_5", "XOR_6").
edge("XOR_5", "AND_6").
edge("AND_5", "OR_3").
edge("AND_6", "OR_3").
edge("XOR_6", "Out_bit_2").
edge("A_bit_3", "XOR_7").
edge("A_bit_3", "AND_7").
edge("B_bit_3", "XOR_7").
edge("B_bit_3", "AND_7").
edge("XOR_7", "XOR_8").
edge("XOR_7", "AND_8").
edge("AND_7", "OR_4").
edge("AND_8", "OR_4").
edge("XOR_8", "Out_bit_3").
edge("OR_3", "XOR_8").
edge("OR_3", "AND_8").
edge("OR_2", "XOR_6").
edge("OR_2", "AND_6").
edge("A_bit_4", "XOR_9").
edge("A_bit_4", "AND_9").
edge("B_bit_4", "XOR_9").
edge("B_bit_4", "AND_9").
edge("XOR_9", "XOR_10").
edge("XOR_9", "AND_10").
edge("AND_9", "OR_5").
edge("AND_10", "OR_5").
edge("XOR_10", "Out_bit_4").
edge("A_bit_5", "XOR_11").
edge("A_bit_5", "AND_11").
edge("B_bit_5", "XOR_11").
edge("B_bit_5", "AND_11").
edge("XOR_11", "XOR_12").
edge("XOR_11", "AND_12").
edge("AND_11", "OR_6").
edge("AND_12", "OR_6").
edge("XOR_12", "Out_bit_5").
edge("OR_5", "XOR_12").
edge("OR_5", "AND_12").
edge("A_bit_6", "XOR_13").
edge("A_bit_6", "AND_13").
edge("B_bit_6", "XOR_13").
edge("B_bit_6", "AND_13").
edge("XOR_13", "XOR_14").
edge("XOR_13", "AND_14").
edge("AND_13", "OR_7").
edge("AND_14", "OR_7").
edge("XOR_14", "Out_bit_6").
edge("A_bit_7", "XOR_15").
edge("A_bit_7", "AND_15").
edge("B_bit_7", "XOR_15").
edge("B_bit_7", "AND_15").
edge("XOR_15", "XOR_16").
edge("XOR_15", "AND_16").
edge("AND_15", "OR_8").
edge("AND_16", "OR_8").
edge("XOR_16", "Out_bit_7").
edge("OR_7", "XOR_16").
edge("OR_7", "AND_16").
edge("OR_6", "XOR_14").
edge("OR_6", "AND_14").
edge("OR_4", "XOR_10").
edge("OR_4", "AND_10").
edge("INPUT_Carry", "XOR_2").
edge("INPUT_Carry", "AND_2").
edge("OR_8", "Out_bit_carry").


%% Cardinality constraints:
% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.
{ edge(src, "XOR_1") : neuron("XOR", "XOR_1") } 2.
{ edge(src, "AND_1") : neuron("AND", "AND_1") } 2.
{ edge(src, "XOR_2") : neuron("XOR", "XOR_2") } 2.
{ edge(src, "AND_2") : neuron("AND", "AND_2") } 2.
{ edge(src, "OR_1") : neuron("OR", "OR_1") } 2.
{ edge(src, "XOR_3") : neuron("XOR", "XOR_3") } 2.
{ edge(src, "AND_3") : neuron("AND", "AND_3") } 2.
{ edge(src, "XOR_4") : neuron("XOR", "XOR_4") } 2.
{ edge(src, "AND_4") : neuron("AND", "AND_4") } 2.
{ edge(src, "OR_2") : neuron("OR", "OR_2") } 2.
{ edge(src, "XOR_5") : neuron("XOR", "XOR_5") } 2.
{ edge(src, "AND_5") : neuron("AND", "AND_5") } 2.
{ edge(src, "XOR_6") : neuron("XOR", "XOR_6") } 2.
{ edge(src, "AND_6") : neuron("AND", "AND_6") } 2.
{ edge(src, "OR_3") : neuron("OR", "OR_3") } 2.
{ edge(src, "XOR_7") : neuron("XOR", "XOR_7") } 2.
{ edge(src, "AND_7") : neuron("AND", "AND_7") } 2.
{ edge(src, "XOR_8") : neuron("XOR", "XOR_8") } 2.
{ edge(src, "AND_8") : neuron("AND", "AND_8") } 2.
{ edge(src, "OR_4") : neuron("OR", "OR_4") } 2.
{ edge(src, "XOR_9") : neuron("XOR", "XOR_9") } 2.
{ edge(src, "AND_9") : neuron("AND", "AND_9") } 2.
{ edge(src, "XOR_10") : neuron("XOR", "XOR_10") } 2.
{ edge(src, "AND_10") : neuron("AND", "AND_10") } 2.
{ edge(src, "OR_5") : neuron("OR", "OR_5") } 2.
{ edge(src, "XOR_11") : neuron("XOR", "XOR_11") } 2.
{ edge(src, "AND_11") : neuron("AND", "AND_11") } 2.
{ edge(src, "XOR_12") : neuron("XOR", "XOR_12") } 2.
{ edge(src, "AND_12") : neuron("AND", "AND_12") } 2.
{ edge(src, "OR_6") : neuron("OR", "OR_6") } 2.
{ edge(src, "XOR_13") : neuron("XOR", "XOR_13") } 2.
{ edge(src, "AND_13") : neuron("AND", "AND_13") } 2.
{ edge(src, "XOR_14") : neuron("XOR", "XOR_14") } 2.
{ edge(src, "AND_14") : neuron("AND", "AND_14") } 2.
{ edge(src, "OR_7") : neuron("OR", "OR_7") } 2.
{ edge(src, "XOR_15") : neuron("XOR", "XOR_15") } 2.
{ edge(src, "AND_15") : neuron("AND", "AND_15") } 2.
{ edge(src, "XOR_16") : neuron("XOR", "XOR_16") } 2.
{ edge(src, "AND_16") : neuron("AND", "AND_16") } 2.
{ edge(src, "OR_8") : neuron("OR", "OR_8") } 2.
{ edge(src, "Out_bit_0") : neuron("OUTPUT", "Out_bit_0") } 1.
{ edge(src, "Out_bit_1") : neuron("OUTPUT", "Out_bit_1") } 1.
{ edge(src, "Out_bit_2") : neuron("OUTPUT", "Out_bit_2") } 1.
{ edge(src, "Out_bit_3") : neuron("OUTPUT", "Out_bit_3") } 1.
{ edge(src, "Out_bit_4") : neuron("OUTPUT", "Out_bit_4") } 1.
{ edge(src, "Out_bit_5") : neuron("OUTPUT", "Out_bit_5") } 1.
{ edge(src, "Out_bit_6") : neuron("OUTPUT", "Out_bit_6") } 1.
{ edge(src, "Out_bit_7") : neuron("OUTPUT", "Out_bit_7") } 1.
{ edge(src, "Out_bit_carry") : neuron("OUTPUT", "Out_bit_carry") } 1.


%% Values:
% val(neuron_id, value).
val("INPUT_Carry", 0).
val("A_bit_0", 1).
val("B_bit_0", 1).
val("A_bit_1", 1).
val("A_bit_2", 0).
val("A_bit_3", 0).
val("A_bit_4", 0).
val("A_bit_5", 0).
val("A_bit_6", 0).
val("A_bit_7", 0).
val("B_bit_1", 0).
val("B_bit_3", 0).
val("B_bit_2", 1).
val("B_bit_4", 0).
val("B_bit_5", 0).
val("B_bit_6", 0).
val("B_bit_7", 0).
