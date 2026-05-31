%% gate: NAND
%% inputs: 2
%% outputs: 1

% type("TYPE")
type("NAND").

% gate(TYPE, OUTPUT, INPUTS)
gate("NAND", Out, In1, In2) :-
    values(In1), values(In2),
    Out = 1 - (In1 * In2).