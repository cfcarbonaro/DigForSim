
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


%%%   this makes alibi possible:
%%%   2 different persons say the same thing:
says( tom, at(tom, (4,2), 6) ).
says( john, at(tom, (4,2), 6) ).

says( john, at(john, (8,9), 4) ).
says( john, at(john, (3,9), 5) ).







crime_location( (9,2) ).

crime_time( 7 ).


suspect( tom ).

at( tom, (6,3), 9).


{ reliable( john ) }.


%--------------%--------------%--------------%--------------%--------------
%
%                                Rules
%
%--------------%--------------%--------------%--------------%--------------



%%%   Y gives alibi for X :

gives_alibi( Y, X, S ) :- says( X, S ),
                          says( Y, S ), 
                          X != Y, 
                          S=at( X,L,T ), 
                          in_time_radius( T ),
                          not in_radius( L ) .




%%%   actually a square, around location of crime:
%%%   ( external function (dist_eukl e.g.) may take more time...? )

#const radius = 4.
in_radius( (X', Y') ) :- crime_location( ( X,Y ) ),
                         at( P, ( X',Y' ), T ), 
                         |X-X'| <= radius,
                         |Y-Y'| <= radius .
                

#const time_radius = 4.
in_time_radius( T' )  :-  crime_time( T ),
                          at( P, ( X',Y' ), T' ),
                          |T - T'| <= time_radius .





%%%   I define "reliable" as definitely speaking the truth:

innocent( X ) :- suspect( X ),
                 gives_alibi( Y, X, _ ),
                 reliable( Y ). 
                 
                 
reliable( P )  :-  not suspect( P ) .                 
                 


%%%   10 is dummy-time here ( to standardize statement/3 ):
statement( P, 10, S ) :- says( P, S ).

true( S )  :-  reliable( P ), statement( P, T, S ).

at_( P,L,T ) :-  true( S ), S = at( P,L,T ).



%--------------%--------------%--------------%--------------%--------------

            
{ true( S ) ; false( S ) } = 1  :-  gives_alibi( Y, X, S ), not reliable( Y ).


%%%  statement made by suspect about him/herself may be true or not.
{ at_( P, L, T ) }  :-  statement( P, T', S ),
                        S = at( P, L, T ),
                        suspect( P ).
                      
suspect( john ).                      





%%{ at(P,L,T) } :- gives_alibi( Y, X, S ), says( X, S ), S = at(P,L,T).




 
%--------------%--------------%--------------%--------------%--------------
%
%                               Output
%
%--------------%--------------%--------------%--------------%--------------


#show in_radius/1. 
#show in_time_radius/1. 

#show reliable/1.

#show at/3.
#show at_/3.

#show innocent/1.
#show gives_alibi/3.

%#show statement/3.

#show crime_location/1.
#show crime_time/1.

%#show true/1.
%#show false/1.

