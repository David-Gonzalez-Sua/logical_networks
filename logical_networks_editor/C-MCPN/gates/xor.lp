%% gate: XOR
%% inputs: 2
%% outputs: 1

% type("TYPE")
type("XOR").

% gate(TYPE, OUTPUT, INPUTS)
gate("XOR", Out, In1, In2) :-
    values(In1), values(In2),
    Out = (In1 + In2 - 2 * In1 * In2).