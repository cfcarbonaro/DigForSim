

#const time_tolerance = 4.
#const distance_tolerance = 260.


%--------------%--------------%--------------%--------------%--------------%
%                                                                          |
%                                   Facts                                  |
%                                                                          |
%--------------%--------------%--------------%--------------%--------------%
%                                                                          |
%   please include:                                                        |
%                                                                          |
%   Locations_sam_spade.lp                                                 |
%   external_functions_2.lp                                                |
%                                                                          |
%--------------%--------------%--------------%--------------%--------------%


suspect("tom").

%statement( "tom", 30, at("tom", "Luisenplatz 2, Potsdam", 5) ).

statement( "tom", 30, at("tom", "Brandenburger Straße 20, Potsdam", 5) ).

%%statement("tom",30,at("tom","Luisenplatz 5, Potsdam",5)).
%% crime_place(loc(130,98)).



crime_time(7).
crime_place("Brandenburger Straße 25, Potsdam").

suspect(sam_spade).



%--------------%--------------%--------------%--------------%--------------
%|
%|                                   Rules
%|
%--------------%--------------%--------------%--------------%--------------



%%%  Shortcut
loc(X,Y) :- crime_location(loc(X,Y)).

%%%  if location is only given as string (address) -> fetch loc(X;Y) format:
%fetch_location(L) :- crime_place(L), L != loc(X,Y), loc(X,Y). 
fetch_location(L) :- crime_place(L).

%%%  if fetch_location(L) -> get osm data via nominatim.

%crime_location( @nominatim(L) ) :- crime_place(L).   %%, fetch_location(L).

%%%  fetched location  ( don't overuse OSM-servers ), therefore comment line above!

crime_location(loc(-414,221)).




check(L) :-  crime_time(T),
             suspect(S),
             statement( P, _, at(S, L, T') ),
             |T-T'| <= time_tolerance.



%checked_location( @nominatim(L) )  :-  check(L).
%%%  result of line above:

checked_location(loc(-537,202)).


%%%  If @nominatim() failed to fetch location it returns "None":
loc_of_interest(L) :- checked_location(L), L != "None".  

%%%  A crime location is always location of interest:
loc_of_interest(L) :- crime_location(L).




%%location( @nominatim(L), L ) :-  check(L), not crime_place(L).

%%% crime_location( @nominatim(L) ) :- crime_place(L), check(L).



at(P,loc(X,Y),T) :- at(P,loc(X,Y,_),T).  %% don't care about z-axis for now

loc(X,Y) :- at(P,loc(X,Y),T).



%%% check distance only when time is close to crime time:

check_dist( loc(X,Y), loc(X',Y') ) :- crime_location( loc(X,Y) ), 
                                             suspect(P),
                                             at( P, loc(X',Y'), T' ), 
                                             crime_time(T), 
                                             |T-T'| <= time_tolerance . 


check_dist( L, L' )  :-  loc_of_interest(L), at( P, L', T' ), suspect(P) .

% time_close(T, T',P) :- crime_time(T), |T-T'| <= time_tolerance, at(P,loc(X',Y'),T') .



%%%  Manhattan distance:
dist_manh( |X-X'|, |Y-Y'|, loc(X,Y), loc(X',Y') ) :- check_dist( loc(X,Y), loc(X',Y') ).

                         
close_to(L,L',D,P,T) :- at(P,L',T),
                        %crime_location(L),   %% location of interest (LOI) in general.
                        loc_of_interest(L),
                        dist_eukl(D,L,L'),
                        D <= distance_tolerance.




%--------------%--------------%--------------%--------------%--------------
%|
%|                                   Output
%|
%--------------%--------------%--------------%--------------%--------------

#show check/1.

%#show check_dist/2.
%#show dist_manh/4.
#show fetch_location/1.
#show crime_location/1.
%#show dist_eukl/3.
#show crime_place/1.
#show crime_time/1.

%#show close_to/5.
%#show at/3.

#show checked_location/1.
#show loc_of_interest/1.
%#show loc/2.
