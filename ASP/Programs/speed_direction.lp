%---------------------------------------------
%   Please include:
%
%   init_at.lp
%   external_functions.lp 
%---------------------------------------------


at(P, T) :- at(P, _, T).

time(T..T1) :- at(P,T), at(P,T1), T<T1.
loc(X,Y) :- at( _,loc(X,Y), _).


hasSucc(P, T) :- at(P,T), at(P,T'), T<T', time(T').       %%  has successor
%%hasSucc(P, T) :- at(P,T), at(P,T'), T<T'.       %%  is time/1 necessary at all? - maybe I had this for safety.
hasPre(P, T)  :- at(P,T), at(P,T'), T>T', time(T').       %%  has predecessor
%%hasPre(P, T)  :- at(P,T), at(P,T'), T>T'.       %%  has predecessor

last(P, T)    :- not hasSucc(P,T), at(P,T).
first(P, T)   :- not hasPre(P,T), at(P,T).


0 { succ(P,T,T') : at(P, T') } 1 :- at(P, T), T<T', not last(P,T), time(T').
%%0 { succ(P,T,T') : at(P, T') } 1 :- at(P, T), T<T', not last(P,T), at(P, T').


:- succ(P,T,T1), succ(P,T,T2), T1<T2.
:- succ(P,T1,T), succ(P,T2,T), T1<T2.
:- at(P,T), not last(P,T), not succ(P,T,_).


%%moved(P, loc(X,Y), loc(X',Y'), T, T') :- succ(P, T, T'), at(P, loc(X,Y), T), at(P, loc(X',Y'), T').

moved(P, loc(X,Y), loc(X',Y'), T, T') :- succ(P, T, T'), at(P, loc(X,Y), T), at(P, loc(X',Y'), T'), loc(X',Y')!=loc(X,Y).

{ stayed(P,loc(X,Y),T,T') ; unknown_path(P, loc(X,Y), T, T') } = 1 :- at(P, loc(X,Y), T), at(P, loc(X,Y), T'), succ(P, T, T').

%%{ unknown_path(P, L, L, T, T') } :- stayed(P,L,T,T'), moved( P, L, L, T, T').


dist_manh( |X-X'|, |Y-Y'|, loc(X,Y), loc(X',Y') ) :- moved( P, loc(X,Y), loc(X',Y'), _, _ ).     %% Manhattan distance
dist_eukl( @dist(Xm,Ym), loc(X,Y), loc(X',Y') )   :- dist_manh( Xm,Ym, loc(X,Y), loc(X',Y')).    %% Euclidian distance

%%speed( P, T, T', D, @div(D, T'-T) ) :- moved( P, loc(X,Y), loc(X',Y'), T, T' ), dist_eukl( D, loc(X,Y), loc(X',Y') ), time(T), time(T').

speed( P, T, T', D, @div(D, T'-T) ) :- moved( P, loc(X,Y), loc(X',Y'), T, T' ), dist_eukl( D, loc(X,Y), loc(X',Y') ).

%% if speed is greater than 5 m/s = 18 km/h
needVehicle( P, T, T', S ) :- speed( P, T, T', _, S ), S > 5.  

useVehicle( P, car, T1, T2 ) :- not route( V, loc(X1,Y1), loc(X2,Y2), T1, T2 ), needVehicle( P, T1, T2, S ),
                                vehicle(V), loc(X1,Y1), loc(X2,Y2), not noCar(P, T1, T2).
0{useVehicle( P, V', T1, T2 )}1  :-  route( V, loc(X1,Y1), loc(X2,Y2), T1, T2 ), needVehicle( P, T1, T2, S ), vehicle(V').

%% only choose one vehicle ( should be more in future )
:- useVehicle( P, V, T1, T2 ) , useVehicle( P, V', T1, T2 ), V<V'.


route( tram, loc(277,-35), loc(65,-30), 28, 40 ). 
noCar( "Lucas Guterres", 28, 40 ).


%--------------------  Durations (Time intervals)  ------------%--------------------
%
%   if location doesn't change after smallest time unit ( == 1 ), collapse to time interval!
%%
%--------------------%--------------------%--------------------%--------------------

%statement( p1, 50, content( p1, loc(7, 9), 10) ).

statement( p1, 50, content( stayed("Tom Meyer", loc(2,98), 8, 12) ) ).
%suspect( p1 ).
%reliable( p1 ).

%%  stayed("Tom Meyer",loc(2,98),8,12).   <- this fact reduces answer sets. 


stayed(P,L,T,T') :- statement( _, _, content(C) ), C=stayed(P,L,T,T'), reliable(P') .

%{ stayed(P',L,T,T') } :- statement( P, _, content(C) ), C=stayed(P',L,T,T'), suspect(P).






#show statement/3.
#show reliable/1.
#show suspect/1.


%#show first/2.
%#show last/2.

%#show at/2.
%#show succ/3.
%#show moved/5.

%#show speed/5.
%#show useVehicle/4.

%%#show time/1.
#show stayed/4.
#show unknown_path/4.
