%% Nuerons
nueron(AND_1, AND).
nueron(NOT_1, NOT).
nueron(XOR_1, XOR).

%% Links
link(AND_1, NOT_1, 0).
link(NOT_1, XOR_1, 1).
