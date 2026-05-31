%% gate: INPUT
%% inputs: 0
%% outputs: 1

type("INPUT").

% gate(TYPE, INPUTS, OUTPUTS)
gate("INPUT", [], [Out]) :-
    values(Out).