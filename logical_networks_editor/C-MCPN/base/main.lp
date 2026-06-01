%%% C-MCPN main logic file.

%% Value domain
values(0;1).

%% Gate activations
% Edges carry values from input to output
edge(In, Neuron_id, Val) :-
    edge(In, Neuron_id),
    neuron(_, Neuron_id),
    neuron(_, In),
    val(In, Val).

% 2 input gates
val(Neuron_id, Val) :-
    gate(Type, Val, Val1, Val2),
    neuron(Type, Neuron_id),
    % neuron(_, In1),
    % neuron(_, In2),
    edge(In1, Neuron_id, Val1),
    edge(In2, Neuron_id, Val2),
    In1 != In2.

% 1 input gates
val(Neuron_id, Val) :-
    gate(Type, Val, Val1),
    neuron(Type, Neuron_id),
    edge(In1, Neuron_id, Val1).

% 0 input gates  NOTE: This rule breaks the network...
% val(Neuron_id, Val) :-
%     neuron(Type, Neuron_id),
%     gate(Type, Val).

%% Value constraints
{ val(Neuron_id, Val) : values(Val) } 1 :- neuron(_, Neuron_id).

%% Show Values
#show val/2.