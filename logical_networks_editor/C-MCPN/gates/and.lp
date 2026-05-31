%% gate: AND
%% inputs: 2
%% outputs: 1

% type("TYPE")
type("AND").

% gate(TYPE, OUTPUT, INPUTS)
gate("AND", Out, In1, In2) :-
    values(In1), values(In2),
    Out = (In1 * In2).