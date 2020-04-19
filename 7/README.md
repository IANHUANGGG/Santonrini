Project 7: Implementing the Player Interface and the Rule Checker
================================================================
Batman and Robin

In this directory is our test harness for xrules, featuring our implementation
of the RuleChecker. You can find our tests in the rules-tests directory. To run the 
tests, run `./rules-tests.sh`, optionally with `-v` to have verbose output.

Test Description
----------------
* Test 1 - valid/invalid moves only 
    test moving to a +0 or +1 building -> "no" 
    test moving off board -> "no" 
    test moving to a +2 building -> "no" 
    test move put put -> "no" 
    test move on another worker -> "no" 
    test moving down from a +2 to a 0 high building -> "yes" 
* Test 2 - valid move + valid build 
    test moving to a +1 higher location then building to a +0 high 
    test moving to a +0 location then building to a +3 high 
    test moving down from a 2 high spot to a 0 high spot then building on the 2 high spot 
* Test 3 - valid move + invalid build 
    move then build onto another worker 
    move then build off the board 
    move then build onto a 4 high place 
    move then build on put put 
* Test 4 - Invalid move + valid build 
    move put put -> build 
    move off board -> build on board 
    move +2 high then build 
* Test 5 - Invalid move + invalid board 
    test move put put -> build put put 
    test move on another worker then build on another worker 
    test move move off board then build off board