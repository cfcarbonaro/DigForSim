at(p, loc(3,4), 7).
at(p, loc(4,5), 25).
at(p, loc(6,7), 13).
at(p, loc(4,5), 56).
at(p, loc(6,7), 9).

{moved(P, loc(X,Y), loc(X',Y'), T, T')} :- at(P, loc(X,Y), T), at(P, loc(X',Y'), T'), T<T'.

%%moved(P, loc(X1,Y1), loc(X2,Y2), T1, T2) :- at(P, loc(X1,Y1), T1), at(P, loc(X2,Y2), T2), T1<T, T<T2, not at(P, loc(X,Y), T ).

:- moved(P, _,_,T,T1), moved(P,_,_,T,T2), T1<T2.
:- moved(P, _,_,T1,T), moved(P,_,_,T2,T), T1<T2.
:- at(P, _, T), not moved(P, _,_,T,_), not moved(P,_,_,_,T).
