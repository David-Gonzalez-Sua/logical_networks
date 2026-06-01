%% gate: OUTPUT
%% inputs: 1
%% outputs: 0

% type("TYPE")
type("OUTPUT").

% gate(TYPE, OUTPUT, INPUTS)
gate("OUTPUT", In, In) :-
    values(In).