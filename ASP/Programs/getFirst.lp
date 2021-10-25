at(p, 4).
at(p, 7).
at(p, 14).
at(p, 20).
at(p, 30).

time(T..T1) :- at(P,T), at(P,T1), T<T1.

hasSucc(P, T) :- at(P,T), at(P,T'), T<T', time(T').       %%  has successor
hasPre(P, T)  :- at(P,T), at(P,T'), T>T', time(T').       %%  has predecessor

last(P, T)    :- not hasSucc(P,T), at(P,T).
first(P, T)   :- not hasPre(P,T), at(P,T).


mov(P, T', T)     :- at(P, T), at(P, T'), T>T', not first(P, T).






%mov2(P, T, T')    :- at(P, T), at(P,T'), T<T', not last(P, T).
%%:- at(P, T), not last(P, T).

