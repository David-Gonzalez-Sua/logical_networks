%% gate: NOT
%% inputs: 1
%% outputs: 1

type("NOT").

% gate(TYPE, INPUTS, OUTPUTS)
gate("NOT", [In], [Out]) :-
    values(In),
    Out = 1 - In.