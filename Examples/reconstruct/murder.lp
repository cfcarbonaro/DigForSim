%person(tom).
%person(anton).
%person(lisa).

%at(tom, loc(3,7), 8).
%at(tom, loc(5,10), 5).
%at(tom, loc(13,12), 14).

%at(lisa,loc(20,15),8).
%at(lisa,loc(-8,7),3).
%at(lisa,loc(-10,9),12).

person(lucas_guterres).
person(anna_xing).
person(thief).



{stayAt( anton, loc(8, 12), 11, 34)}.

murder( loc(18, 12), 14 ). 




suspect( P ) :- stayAt( P, L, T1, T2 ), murder( L, T ), T>=T1, T<=T2.

suspect( P ) :- at( P, L, T ), murder( L, T' ), T=T'.





