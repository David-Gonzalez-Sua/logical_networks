%% gate: NOT
%% inputs: 1
%% outputs: 1

% gate(TYPE, INPUTS, OUTPUTS)
gate("not", [In], [Out]) :-
    values(In),
    Out = 1 - In.