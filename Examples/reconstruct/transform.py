# transform typical clingo output in only Answer Sets part 
# Cuts away additional technical information.

#path_read  = "/home/j/Schreibtisch/o.log"
#path_write = "/home/j/Schreibtisch/i.log"

path_read = "./o.log"
path_write = "./i.log"



with open(path_read, "r") as f_r:
	
	with open(path_write, "w") as f_w: 
		answer = 0
		for l in f_r.readlines():
			
			if l.startswith("Answer:"):
				answer = 1  # toggle: write lines between two answers to file
				
			if l.startswith("SATISFIABLE"):
				answer = 0

			if answer == 1:
				f_w.write(l)


		
