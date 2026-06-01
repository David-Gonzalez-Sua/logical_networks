%% gate: OUTPUT
%% inputs: 1
%% outputs: 1

% type("TYPE")
type("OUTPUT").

% gate(TYPE, OUTPUT, INPUTS)
gate("OUTPUT", In, In) :-
    values(In).