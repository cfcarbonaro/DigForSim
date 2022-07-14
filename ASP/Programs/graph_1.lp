
edge( 1, 2 ).
edge( 2, 3 ).
edge( 3, 4 ).

edge( 3, 5 ).
edge( 5, 6 ).
edge( 6, 2 ).

edge( 3, 7 ).
edge( 7, 8 ).

edge( 8, 9 ).
edge( 8, 10 ).

%%% big loop:
edge( 10, 4 ).

edge( X, Y )  :-  edge( Y, X ).

vert( X; Y )  :-  edge( X, Y ).

start( 1 ).

end( 7 ).

1 { path( X, Y ) : edge( X, Y ) } 1  :-  start( X ) .


has_input( Y, from( X ) )  :-  path( X, Y ) .


wp( X )  :-  edge( X, Y1 ),  edge( X, Y2 ),  edge( X, Y3 ),  Y1 < Y2,  Y2 < Y3 . 



path( Y, Z )  :-  path( X, Y ), edge( Y, Z ),  X != Z, not path( Z, Y ), not wp( Y ).
                  

%edge( Y, Z ), has_input( Z, from(I) ), vert(I), I != Y


%0 { path( X, Y ) : edge( X, Y ) } 1  :-  wp( X ).

0 { path( X, Y ) : edge( X, Y ) } 1  :-  wp( X ), not path( Y, X ), vert( Y ), path( Z, X ), Z != Y.

%1 { test( X, Y ) : edge( X, Y ) } 1  :-  wp( X ), path( Y, X ).
%path( X, Y )  :-  test( X, Y ).

two_outputs( X, to( Y ), to( Z ) )  :-  path( X, Y ),  path( X, Z ),  Y != Z.

:-  two_outputs( _, _, _ ).

%:-  has_input( X, from( Y1 ) ),  has_input( X, from( Y2 ) ),  Y1 != Y2 .


goal( reached )  :-  path( X, Y ), end( Y ).

:- not goal( reached ).


#show path/2.

%#show two_outputs/3.

%#show has_input/2.

%#show test/2.
