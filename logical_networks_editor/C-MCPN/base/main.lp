% File defining C-MCPN shared values and constraints.

values(0;1).
% type("INPUT";"OUTPUT";"AND";"OR";"NOT";"XOR";"NAND").

1 { val(Type, Val) : type(Type), values(Val) } 1.

% val(Neuron, Val) :- 
%     neuron(Neuron, Type),
%     edge(Inputs, Neuron),
%     gate(Type, Inputs, Outputs),

% 2 input gates
val(Neuron, Val) :-
    gate(Type, Val, Val1, Val2),
    neuron(Neuron, Type),
    neuron(In1, _),
    neuron(In2, _), 
    edge(In1, Neuron),
    edge(In2, Neuron),
    val(In1, Val1),
    val(In2, Val2),
    In1 != In2.

% 1 input gates
val(Neuron, Val) :-
    gate(Type, Val, ValIn),
    neuron(Neuron, Type),
    neuron(In, _),
    edge(In, Neuron),
    val(In, ValIn).

% 0 input gates
val(Neuron, Val) :-
    neuron(Neuron, Type),
    gate(Type, Val).


#show val/2.
% #show *.