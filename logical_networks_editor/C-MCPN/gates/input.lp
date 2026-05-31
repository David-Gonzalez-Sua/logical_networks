%% gate: INPUT
%% inputs: 0
%% outputs: 1

% type("TYPE")
type("INPUT").

% gate(TYPE, OUTPUT, INPUTS)
gate("INPUT", Out) :-
    values(Out).