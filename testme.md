Testing Santorini
=================

To run our unit tests for things we've implemented in Santorini, there are a few steps to take. 

We implemented our unit tests with the `unittest` module in Python and run them using `pytest`. To run our unit tests on the command line, clone this repo and navigate 
to the `Santorini` directory. There, execute the command `python3.6 -m pytest --cov=. Tests`. It's crucial that
you use python3 as we have written everything in this version of the language. If pytest is not already
installed, run `pip3.6 install pytest`. The output that you'll see from pytest is the files that have been
tested, how much time was spent in executing these tests relative to the total time of the run (as a percentage), and how many tests passed in the total time run.

To run our integration tests, we have bash scripts written in their respective project directories, `board-tests.sh` in the `6/` directory and `rules-tests.sh` in the `7/` directory. To see more verbose results, run the script using 
the `-v` option to see actual output vs expected output.