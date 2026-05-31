%% gate: OR
%% inputs: 2
%% outputs: 1

type("OR").

% gate(TYPE, INPUTS, OUTPUTS)
gate("OR", [In1, In2], [Out]) :-
    values(In1), values(In2),
    Out = (In1 + In2 - In1 * In2).