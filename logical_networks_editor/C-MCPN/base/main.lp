% File defining C-MCPN shared values and constraints.

values(0;1).
% type("INPUT";"OUTPUT";"AND";"OR";"NOT";"XOR";"NAND").

% 1 { val(Type, Val) : type(Type), values(Val) } 1.

% 2 input gates
% val(Neuron_id, Val) :-
%     gate(Type, Val, Val1, Val2),
%     neuron(Type, Neuron_id),
%     neuron(_, In1),
%     neuron(_, In2), 
%     edge(In1, Neuron_id),
%     edge(In2, Neuron_id),
%     val(In1, Val1),
%     val(In2, Val2).
    % In1 != In2.

% 1 input gates
% val(Neuron_id, Val, Val1) :-
%     neuron(Type, Neuron_id),
%     neuron(_, In),
%     gate(Type, Val, Val1),
%     edge(In, Neuron_id),
%     val(In, Val1).

% 0 input gates
val(Neuron_id, Val) :-
    neuron(Type, Neuron_id),
    gate(Type, Val).


% Value constraints
% 1 { val(Neuron, Val) : values(Val) } 1 :- type(Type).
% 1 { val(Neuron, Val) : values(Val) } 1 :- neuron(Type, Neuron), type(Type).
% 1 { val(Neuron, Val) : neuron(_, Neuron) } 1 :- values(Val).
{ val(Neuron_id, Val) : values(Val) } 1 :- neuron(_, Neuron_id).


%#show edge/2.
#show val/2.
% #show *.
%#show neuron/2.