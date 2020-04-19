Project 6: Implementing Common Pieces
=====================================
Batman and Robin

There are three main things in this project directory. 

The first is xboard, which is our system-level test harness for Santorini. Our tests for it
can be run using ./board-tests.sh, and the '-v' option is left for verbose printing of tests. 
Xboard reads commands from standard in with a new line as a delimiter, and passes them along
to our implementation. 

The second is board-tests, which features 5 tests for Santorini to be used with xboard. In it
are five tests with different board states and commands, all with accompanying expected output.

The third is board-tests.sh, which is the script for running all of these in conjunction. To use it, 
run `./board-tests.sh` on the command line.