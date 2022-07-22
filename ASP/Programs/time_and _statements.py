#show dim/1.

#show stayed/4.
#show -stayed/4.
#show time_delta/1.
#show statement/3.


at( "John", 450, loc( 30, 42 ) ) .

contradiction( P, T )  :-  stayed( P, T1, T2, L ),  at( P, T, L' ),  L != L',  T1 < T,  T < T2.


statement( "Tommy", "2022-06-09 16:11:00", content( stayed( "John", -200, 1600, loc( 10, 12 ) ) ) ).

{ -stayed( P', T1, T2, L ) ; stayed( P', T1, T2, L ) } = 1   :-  statement( P, T, content(C) ),
                                  C=stayed( P', T1, T2, L ) .
                                  
                                  
%works(yes)  :-  statement( P, T, content(C) ), -C.






%%% base time :

base_time( "2022-06-05 12:30:00" ).



%%%  External function for time conversion:

#include "External_functions/time_functions.py".



time_delta( @time( "2022-06-05 12:45:00", "2022-06-05 12:50:00" ) ).
