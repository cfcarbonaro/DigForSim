#!/bin/bash
echo Running temporary clingo.
source /home/j/anaconda3/bin/activate asp && \
clingo 0 /home/j/DigForSim/ASP/temp_clingo.lp > /home/j/DigForSim/ASP/out.log && \ #>> /home/j/DigForSim/Test_System/out.log && \
echo hallo nochmal
