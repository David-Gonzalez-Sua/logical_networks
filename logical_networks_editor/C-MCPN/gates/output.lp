%% gate: OUTPUT
%% inputs: 1
%% outputs: 0

type("OUTPUT").

% gate(TYPE, INPUTS, OUTPUTS)
gate("OUTPUT", [In], []) :-
    values(In).