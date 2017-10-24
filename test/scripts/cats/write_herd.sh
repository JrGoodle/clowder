#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo "TEST: Test clowder herd write"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh
./init.sh

if [ "$ACCESS_LEVEL" == "write" ]; then
    test_herd_rebase_conflict() {
        print_single_separator
        echo "TEST: clowder herd rebase conflict"
        clowder link || exit 1
        clowder herd $PARALLEL || exit 1

        pushd mu || exit 1
        touch rebasefile || exit 1
        echo 'something' >> rebasefile
        git add rebasefile || exit 1
        git commit -m 'Add rebase file' || exit 1
        git push || exit 1
        git reset --hard HEAD~1 || exit 1
        touch rebasefile || exit 1
        echo 'something else' >> rebasefile
        git add rebasefile || exit 1
        git commit -m 'Add another rebase file' || exit 1
        test_no_rebase_in_progress
        popd || exit 1

        clowder herd $PARALLEL -r && exit 1

        pushd mu || exit 1
        test_rebase_in_progress
        popd || exit 1

        clowder clean -a || exit 1

        pushd mu || exit 1
        test_no_rebase_in_progress
        git reset --hard HEAD~1 || exit 1
        git push --force || exit 1
        popd || exit 1
    }
    test_herd_rebase_conflict
fi
