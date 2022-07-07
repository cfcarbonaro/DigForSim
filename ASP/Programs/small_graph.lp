
edge(1, 2, 4).
edge(1, 3, 3).
edge(2, 4, 6).
edge(3, 4, 5).
edge(4, 5, 7).

edge(5, 6, 4).

edge(1, 7, 5).
edge(7, 8, 4).
edge(7, 9, 4).


edge( Y, X, W )  :-  edge( X, Y, W ).

vert( X; Y )  :-  edge( X, Y, _ ).



start( 1 ).




%%%---------  Find waypoint with clingo  ---------------

wp( X )  :-  edge( X, Y, _ ),  edge( X, Y', _ ),  edge( X, Y'', _ ),  Y < Y', Y' < Y'' , not start( X ).     %%%  yields:   wp( 7 ). wp( 4 ).

wp( X, from( Y ), W )  :-  wp( X ), path( Y, X, W ).




1 { path( X, Y, W ) : edge( X, Y, W ) } 1   :-   start( X ) .


1 { path( X, Y, W + W' ) : edge( X, Y, W )  } 1   :-   wp( X, from( Z ), W' ) .


path( Y, Z, W + W' )  :-  path( X, Y, W ),  edge( Y, Z, W' ),  X != Z,  not wp( Y ),  not start( Z ).



:-  path( X, Y, _ ), path( Y, X, _ ).

:-  path( X, Y, W ), path( X, Y, W' ), W != W'.




#show path/3.

#show wp/3.

#show goal/1.
