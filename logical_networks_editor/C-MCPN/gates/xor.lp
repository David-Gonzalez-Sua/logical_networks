%% gate: XOR
%% inputs: 2
%% outputs: 1

type("XOR").

% gate(TYPE, INPUTS, OUTPUTS)
gate("XOR", [In1, In2], [Out]) :-
    values(In1), values(In2),
    Out = (In1 + In2 - 2 * In1 * In2).