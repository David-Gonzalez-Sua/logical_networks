%% gate: NAND
%% inputs: 2
%% outputs: 1

type("NAND").

% gate(TYPE, INPUTS, OUTPUTS)
gate("NAND", [In1, In2], [Out]) :-
    values(In1), values(In2),
    Out = 1 - (In1 * In2).