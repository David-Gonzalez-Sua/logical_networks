%% gate: NOT
%% inputs: 1
%% outputs: 1

% type("TYPE")
type("NOT").

% gate(TYPE, OUTPUT, INPUTS)
gate("NOT", Out, In) :-
    values(In),
    Out = 1 - In.