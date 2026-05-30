%% gate: OUTPUT
%% inputs: 1
%% outputs: 0

% gate(TYPE, INPUTS, OUTPUTS)
gate(output, [In], []) :-
    values(In).