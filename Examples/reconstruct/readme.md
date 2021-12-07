In this directory are already generated files (the agents log-files e.g., o.log , i.log,..)


**To try it yourself, follow these steps:

1) Run simulation in UPBGE (2.79)
(This generates log-data, that already get a lp-extension

2) run Clingo with the files:
  murder.lp (bytheway it's not a murder:)
  <agents>_log.lp
  
  and output it to a file o.log
  
  (Answer set(s) are going to be created in that file )

3) Use transform.py to convert o.log in i.log 
   ( it's the same like o.log without the technical output information of Clingo )
  
4) Run reconstruct in UPBGE:
   
  inside UPBGE run the two scripts:
  1) import_asp_log.py 
      ( imports i.log and uses regular expressions, then pickles an dictionary )
  2) load_answer_sets.py
      ( loads the pickled dict and starts creating the game objects )
  
  
  
  
  
