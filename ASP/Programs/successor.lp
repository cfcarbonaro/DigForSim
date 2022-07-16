at(p, 4). at(p, 6). at(p, 7). at(p, 13). at(p, 21).
at(p1, 4).
at(p1, 7).
at(p1, 14).
at(p1, 20).
at(p1, 30).
at( p2, 11 ).

time(T..T1) :- at(P,T), at(P,T1), T<T1.


hasSucc(P, T) :- at(P,T), at(P,T'), T<T', time(T').       %%  has successor
hasPre(P, T)  :- at(P,T), at(P,T'), T>T', time(T').       %%  has predecessor

last(P, T)    :- not hasSucc(P,T), at(P,T).
first(P, T)   :- not hasPre(P,T), at(P,T).


0 { succ(P,T,T') : at(P, T') } 1 :- at(P, T), T<T', not last(P,T), time(T').


:- succ(P,T,T1), succ(P,T,T2), T1<T2.
:- succ(P,T1,T), succ(P,T2,T), T1<T2.
:- at(P,T), not last(P,T), not succ(P,T,_).

#show first/2.
#show last/2.
#show at/2.
#show succ/3.

