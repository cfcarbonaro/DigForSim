
%at( tom, (4,2), 6).

at( tom, (4,2), 9).

%at( anna, (5,5), 2).
at(tom,(-9,-5),0).
at(tom,(-4,-3),2).
at(tom,(10,-4),4).
at(tom,(-4,7),6).
at(tom,(8,-7),8).
at(tom,(-10,3),10).
at(tom,(10,-3),12).
at(tom,(3,-7),14).
at(tom,(9,-5),16).
at(tom,(-3,2),18).



%suspect(tom).
suspect(john).

says(john, at(tom,(-8,10),0)).
says(john, at(tom,(4,1),2)).
says(john, at(tom,(-8,-10),4)).
says(john, at(tom,(8,9),6)).
says(john, at(tom,(8,-2),8)).
says(john, at(tom,(-10,-9),10)).
says(john, at(tom,(1,5),12)).
says(john, at(tom,(10,3),14)).
says(john, at(tom,(8,-9),16)).
says(john, at(tom,(-1,-6),18)).
says( tom, at(tom, (4,2), 6) ).



says( john, at(tom, (4,2), 6) ).
says( john, at(john, (8,9), 4) ).
says( john, at(john, (3,9), 5) ).

% Y gives alibi for X
alibi( Y, X, S ) :- says( X, S ), says( Y, S ), X>Y, S=at(X,_,_).

%{ at(P,L,T) } :- alibi( S ), says( X, S ), S=at(P,L,T).

% print out at() only for suspects ( to not create too many at/3 )
% Choice rule to create 2 worlds: when statement true and when statement is not true
{ at(P,L,T) } :- statement( S ), S=at(P,L,T), suspect(P).


statement(S) :- says( _, S).


innocent( X ) :- suspect( X ), alibi( Y, X, S ), not suspect( Y ).




#show at/3.
#show innocent/1.
#show alibi/3.
#show statement/1.
