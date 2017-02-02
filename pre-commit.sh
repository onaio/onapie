#!/bin/sh
# pre-commit.sh
# Check flake8
echo "Flake8 running. Fix the errors below"
find . -iname "*.py" |grep -v setup.py | xargs flake8 --max-complexity=10

git stash -q --keep-index

FILES_PATTERN='\.py(\..+)?$'
FORBIDDEN='import\s*\S*pdb'
git diff --cached --name-only | \
    grep -E $FILES_PATTERN | \
    GREP_COLOR='4;5;37;41' xargs grep --color --with-filename -n $FORBIDDEN && \
    echo 'COMMIT REJECTED. Found "$FORBIDDEN" references. Please remove them before committing' && exit 1

nosetests tests --with-doctest
RESULT=$?
git stash pop -q
[ $RESULT -ne 0 ] && exit 1
exit 0

