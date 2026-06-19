%% Network Structure
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
neuron("INPUT", "INPUT_Carry").
neuron("INPUT", "INPUT_3").
neuron("XOR", "XOR_3").
neuron("AND", "AND_3").
neuron("INPUT", "INPUT_4").
neuron("XOR", "XOR_4").
neuron("AND", "AND_4").
neuron("OR", "OR_2").
neuron("OUTPUT", "OUTPUT_2").
neuron("XOR", "XOR_5").
neuron("AND", "AND_5").
neuron("XOR", "XOR_6").
neuron("AND", "AND_6").
neuron("OR", "OR_3").
neuron("OUTPUT", "OUTPUT_3").
neuron("XOR", "XOR_7").
neuron("AND", "AND_7").
neuron("XOR", "XOR_8").
neuron("AND", "AND_8").
neuron("OR", "OR_4").
neuron("OUTPUT", "OUTPUT_4").
neuron("INPUT", "INPUT_5").
neuron("INPUT", "INPUT_6").
neuron("INPUT", "INPUT_7").
neuron("INPUT", "INPUT_8").


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
edge("INPUT_3", "XOR_3").
edge("INPUT_3", "AND_3").
edge("INPUT_4", "XOR_3").
edge("INPUT_4", "AND_3").
edge("AND_3", "OR_2").
edge("AND_4", "OR_2").
edge("XOR_4", "OUTPUT_2").
edge("XOR_3", "XOR_4").
edge("XOR_3", "AND_4").
edge("OR_1", "XOR_4").
edge("OR_1", "AND_4").
edge("INPUT_5", "XOR_5").
edge("INPUT_5", "AND_5").
edge("INPUT_6", "XOR_5").
edge("INPUT_6", "AND_5").
edge("AND_5", "OR_3").
edge("AND_6", "OR_3").
edge("XOR_6", "OUTPUT_3").
edge("INPUT_7", "XOR_7").
edge("INPUT_7", "AND_7").
edge("INPUT_8", "XOR_7").
edge("INPUT_8", "AND_7").
edge("AND_7", "OR_4").
edge("AND_8", "OR_4").
edge("XOR_8", "OUTPUT_4").
edge("XOR_7", "XOR_8").
edge("XOR_7", "AND_8").
edge("OR_3", "XOR_8").
edge("OR_3", "AND_8").
edge("XOR_5", "XOR_6").
edge("XOR_5", "AND_6").
edge("OR_2", "AND_6").


%% Cardinality constraints:
% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.
{ edge(src, "XOR_1") : neuron("XOR", "XOR_1") } 2.
{ edge(src, "AND_1") : neuron("AND", "AND_1") } 2.
{ edge(src, "XOR_2") : neuron("XOR", "XOR_2") } 2.
{ edge(src, "AND_2") : neuron("AND", "AND_2") } 2.
{ edge(src, "OR_1") : neuron("OR", "OR_1") } 2.
{ edge(src, "OUTPUT_1") : neuron("OUTPUT", "OUTPUT_1") } 1.
{ edge(src, "XOR_3") : neuron("XOR", "XOR_3") } 2.
{ edge(src, "AND_3") : neuron("AND", "AND_3") } 2.
{ edge(src, "XOR_4") : neuron("XOR", "XOR_4") } 2.
{ edge(src, "AND_4") : neuron("AND", "AND_4") } 2.
{ edge(src, "OR_2") : neuron("OR", "OR_2") } 2.
{ edge(src, "OUTPUT_2") : neuron("OUTPUT", "OUTPUT_2") } 1.
{ edge(src, "XOR_5") : neuron("XOR", "XOR_5") } 2.
{ edge(src, "AND_5") : neuron("AND", "AND_5") } 2.
{ edge(src, "XOR_6") : neuron("XOR", "XOR_6") } 2.
{ edge(src, "AND_6") : neuron("AND", "AND_6") } 2.
{ edge(src, "OR_3") : neuron("OR", "OR_3") } 2.
{ edge(src, "OUTPUT_3") : neuron("OUTPUT", "OUTPUT_3") } 1.
{ edge(src, "XOR_7") : neuron("XOR", "XOR_7") } 2.
{ edge(src, "AND_7") : neuron("AND", "AND_7") } 2.
{ edge(src, "XOR_8") : neuron("XOR", "XOR_8") } 2.
{ edge(src, "AND_8") : neuron("AND", "AND_8") } 2.
{ edge(src, "OR_4") : neuron("OR", "OR_4") } 2.
{ edge(src, "OUTPUT_4") : neuron("OUTPUT", "OUTPUT_4") } 1.


%% Values:
% val(neuron_id, value).
val("INPUT_1", 1).
val("XOR_1", 0).
val("AND_1", 1).
val("INPUT_2", 1).
val("XOR_2", 0).
val("AND_2", 0).
val("OR_1", 1).
val("OUTPUT_1", 0).
val("INPUT_Carry", 0).
