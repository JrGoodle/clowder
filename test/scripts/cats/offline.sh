#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/jules' )

enable_network_connection() {
    case "$(uname)" in
        Linux*)
            print_double_separator
            echo "Enable network connection"
            nmcli nm enable true
            print_double_separator
            ;;
        Darwin*)
            print_double_separator
            echo "Enable network connection"
            networksetup -setairportpower airport on
            print_double_separator
            ;;
        *)
            echo "Offline test only runs on macOS and Ubuntu"
            exit
            ;;
    esac
}

disable_network_connection() {
    case "$(uname)" in
        Linux*)
            print_double_separator
            echo "Disable network connection"
            nmcli nm enable false
            print_double_separator
            ;;
        Darwin*)
            print_double_separator
            echo "Disable network connection"
            networksetup -setairportpower airport off
            print_double_separator
            ;;
        *)
            echo "Offline test only runs on macOS and Ubuntu"
            exit
            ;;
    esac
}

enable_connection_exit() {
    enable_network_connection
    exit 1
}

# echo 'Make sure your network connection is enabled'
# # https://unix.stackexchange.com/a/293941
# read -n 1 -s -r -p "Press any key to continue"
# echo ''
# echo ''
enable_network_connection

print_double_separator
echo "TEST: Test clowder offline"

cd "$CATS_EXAMPLE_DIR" || exit 1
./clean.sh || exit 1
./init.sh || exit 1
clowder herd $PARALLEL || exit 1

# echo 'Disable your network connection'
# # https://unix.stackexchange.com/a/293941
# read -n 1 -s -r -p "Press any key to continue"
# echo ''
# echo ''
disable_network_connection

print_single_separator
echo 'TEST: clowder branch'
clowder branch || enable_connection_exit
print_single_separator
echo 'TEST: clowder branch -r'
clowder branch -r || enable_connection_exit
print_single_separator
echo 'TEST: clowder branch -a'
clowder branch -a || enable_connection_exit
print_single_separator
echo 'TEST: clowder checkout'
clowder checkout branch_name || enable_connection_exit
print_single_separator
echo 'TEST: clowder clean'
clowder clean || enable_connection_exit
print_single_separator
echo 'TEST: clowder diff'
clowder diff || enable_connection_exit
print_single_separator
echo 'TEST: clowder forall'
clowder forall $PARALLEL -c 'git status' || enable_connection_exit
print_single_separator
echo 'TEST: clowder herd'
clowder herd && enable_connection_exit
print_single_separator
echo 'TEST: clowder link'
clowder link -v v0.1 || enable_connection_exit
clowder link || enable_connection_exit
print_single_separator
echo 'TEST: clowder prune'
clowder prune branch || enable_connection_exit
print_single_separator
echo 'TEST: clowder prune -r'
clowder prune -r branch && enable_connection_exit
print_single_separator
echo 'TEST: clowder prune -a'
clowder prune -a branch && enable_connection_exit
print_single_separator
echo 'TEST: clowder repo add'
clowder repo add . || enable_connection_exit
print_single_separator
echo 'TEST: clowder repo checkout'
clowder repo checkout tags || enable_connection_exit
clowder repo checkout master || enable_connection_exit
print_single_separator
echo 'TEST: clowder repo clean'
clowder repo clean || enable_connection_exit
print_single_separator
echo 'TEST: clowder repo commit'
pushd .clowder || exit 1
touch newfile || enable_connection_exit
git add newfile || enable_connection_exit
popd || exit 1
clowder repo commit 'Add newfile' || enable_connection_exit
pushd .clowder || exit 1
git reset --hard HEAD~1 || enable_connection_exit
popd || exit 1
print_single_separator
echo 'TEST: clowder repo pull'
clowder repo pull && enable_connection_exit
print_single_separator
echo 'TEST: clowder repo push'
clowder repo push && enable_connection_exit
print_single_separator
echo 'TEST: clowder repo run'
clowder repo run 'git status' || enable_connection_exit
print_single_separator
echo 'TEST: clowder repo status'
clowder repo status || enable_connection_exit
print_single_separator
echo 'TEST: clowder save'
clowder save offline_version || enable_connection_exit
print_single_separator
echo 'TEST: clowder start'
clowder start local_branch || enable_connection_exit
for project in "${all_projects[@]}"; do
    pushd $project || exit 1
    test_branch 'local_branch'
    popd || exit 1
done
print_single_separator
echo 'TEST: clowder start -t'
clowder start -t tracking_branch && enable_connection_exit
print_single_separator
echo 'TEST: clowder stash'
clowder stash || enable_connection_exit
print_single_separator
echo 'TEST: clowder status'
clowder status || enable_connection_exit
print_single_separator
echo 'TEST: clowder status -f'
clowder status -f && enable_connection_exit
print_single_separator
echo 'TEST: clowder sync'
clowder sync && enable_connection_exit
print_single_separator
echo 'TEST: clowder init'
rm -rf .clowder || enable_connection_exit
clowder init git@github.com:JrGoodle/cats.git && enable_connection_exit
print_single_separator

# echo 'You can enable your network connection again'
# echo ''
enable_network_connection
