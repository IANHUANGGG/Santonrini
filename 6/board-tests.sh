#!/bin/bash

dir=$(dirname "$0")
VERBOSE=false

if [[ $1 == -v* ]]; then
    VERBOSE=true
fi

log() {
    if $VERBOSE; then
        echo -e $1
    fi
}

execute() {
    if ! $VERBOSE; then
        $1 &>/dev/null
    else
        $1
    fi
}

TESTDIR=$dir/board-tests-class/**/*-in.json
#TESTDIR=$dir/board-tests/*-in.json
BIN=$dir/xboard

declare -i passed=0
declare -i failed=0
shopt -s nullglob
tests=($TESTDIR)
total=${#tests[@]}

for t in ${tests[@]}; do
    mkdir -p "$(dirname $t)-out"
    number=$(basename -s -in.json $t)
    $BIN < $t > $(dirname $t)-out/${number}-out.json
    execute "diff -B --strip-trailing-cr -y $(dirname $t)-out/${number}-out.json $(dirname $t)/${number}-out.json"
    if [ $? -eq 0 ]
    then
        log "\033[0;34m$testname \033[0m- \033[1;32m[Test Passed]\033[0m - $t"
        passed+=1
    else
        log "\033[0;34m$testname \033[0m- \033[1;31m[Test Failed]\033[0m - $t"
        failed+=1
    fi
done

echo -e "\033[1;32mPassing: \033[0m$passed"
echo -e "\033[1;31mFailing: \033[0m$failed"
