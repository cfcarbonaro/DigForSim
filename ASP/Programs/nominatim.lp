#const time_tolerance = 9.
#const distance_tolerance = 300.


%--------------%--------------%--------------%--------------%--------------
%|
%|                                   Facts
%|
%--------------%--------------%--------------%--------------%--------------


suspect("tom").

statement("tom",30,at("tom","Luisenplatz 2, Potsdam",5)).
statement("tom",30,at("tom","Luisenplatz 5, Potsdam",5)).

suspect(sam_spade).

crime_time(7).
crime_place("Brandenburger Straße 20, Potsdam").
%crime_place(loc(130,98)).


%--------------%--------------%--------------%--------------%--------------
%|
%|                                   Rules
%|
%--------------%--------------%--------------%--------------%--------------

%%%  Shortcut
loc(X,Y) :- crime_place(loc(X,Y)).


%%%  if location is only given as string (address) -> fetch loc(X;Y) format:
%fetch_location(L) :- crime_place(L), L != loc(X,Y), loc(X,Y). 
fetch_location(L) :- crime_place(L).

%%%  if fetch_location(L) -> get osm data via nominatim.
crime_location( @nominatim(L) ) :- crime_place(L), fetch_location(L).


check(L) :- crime_place(L).

check(L) :- crime_time(T), suspect(S), statement(P,_,at(S,L,T')).


%%location(@nominatim(L), L) :-  check(L), not crime_place(L).

%%% crime_location(@nominatim(L)) :- crime_place(L), check(L).
check_dist(loc(X,Y),loc(X',Y')) :- crime_place(loc(X,Y)), suspect(P), at(P,loc(X',Y',_),T'), 
                                   crime_time(T), |T-T'|<=time_tolerance. 

close_to(L,L',D,P,T) :- at(P,L,T),  D <= distance_tolerance, dist_eukl(D,L,L').
close_to(L,L',D,P,T) :- at(P,L',T),  D <= distance_tolerance, dist_eukl(D,L,L').


at(P,loc(X,Y),T) :- at(P,loc(X,Y,_),T).  %% don't care about z-axis for now

close(D) :- dist_eukl(D,L,L'), D<=distance_tolerance, at(P,L,T) .


%--------------%--------------%--------------%--------------%--------------
%|
%|                                   Output
%|
%--------------%--------------%--------------%--------------%--------------

%%#show check_dist/2.
%%#show dist_manh/4.
#show fetch_location/1.
#show crime_location/1.
#show dist_eukl/3.
#show crime_place/1.
#show crime_time/1.
#show close_to/5.

#show close/1.
