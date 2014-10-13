# pre-commit.sh
git stash -q --keep-index

FILES_PATTERN='\.py(\..+)?$'
FORBIDDEN='import\spdb'
git diff --cached --name-only | \
    grep -E $FILES_PATTERN | \
    GREP_COLOR='4;5;37;41' xargs grep --color --with-filename -n $FORBIDDEN && echo 'COMMIT REJECTED Found "$FORBIDDEN" references. Please remove them before committing' && exit 1

nosetests tests --with-doctest --with-coverage
RESULT=$?
git stash pop -q
[ $RESULT -ne 0 ] && exit 1
exit 0
