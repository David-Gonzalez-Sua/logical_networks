%% gate: OR
%% inputs: 2
%% outputs: 1

% type("TYPE")
type("OR").

% gate(TYPE, OUTPUT, INPUTS)
gate("OR", Out, In1, In2) :-
    values(In1), values(In2),
    Out = (In1 + In2 - In1 * In2).