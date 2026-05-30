%% gate: AND
%% inputs: 2
%% outputs: 1

% gate(TYPE, INPUTS, OUTPUTS)
gate(and, [In1, In2], [Out]) :-
    values(In1), values(In2),
    Out = (In1 * In2).