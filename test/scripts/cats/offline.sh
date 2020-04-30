#!/usr/bin/env bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

export all_projects=( 'mu' 'duke' \
                      'black-cats/kit' \
                      'black-cats/kishka' \
                      'black-cats/sasha' \
                      'black-cats/june' )

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
./clean.sh
./copy-cache.sh

# echo 'Disable your network connection'
# # https://unix.stackexchange.com/a/293941
# read -n 1 -s -r -p "Press any key to continue"
# echo ''
# echo ''
disable_network_connection

print_single_separator
echo 'TEST: clowder branch'
$COMMAND branch || enable_connection_exit
print_single_separator
echo 'TEST: clowder branch -r'
$COMMAND branch -r || enable_connection_exit
print_single_separator
echo 'TEST: clowder branch -a'
$COMMAND branch -a || enable_connection_exit
print_single_separator
echo 'TEST: clowder checkout'
$COMMAND checkout branch_name || enable_connection_exit
print_single_separator
echo 'TEST: clowder clean'
$COMMAND clean || enable_connection_exit
print_single_separator
echo 'TEST: clowder diff'
$COMMAND diff || enable_connection_exit
print_single_separator
echo 'TEST: clowder forall'
$COMMAND forall $PARALLEL -c 'git status' || enable_connection_exit
print_single_separator
echo 'TEST: clowder herd'
$COMMAND herd && enable_connection_exit
print_single_separator
echo 'TEST: clowder link'
$COMMAND link -v v0.1 || enable_connection_exit
$COMMAND link || enable_connection_exit
print_single_separator
echo 'TEST: clowder prune'
$COMMAND prune branch || enable_connection_exit
print_single_separator
echo 'TEST: clowder prune -r'
$COMMAND prune -r branch && enable_connection_exit
print_single_separator
echo 'TEST: clowder prune -a'
$COMMAND prune -a branch && enable_connection_exit
print_single_separator
echo 'TEST: clowder repo add'
$COMMAND repo add . || enable_connection_exit
print_single_separator
echo 'TEST: clowder repo checkout'
$COMMAND repo checkout repo-test || enable_connection_exit
$COMMAND repo checkout master || enable_connection_exit
print_single_separator
echo 'TEST: clowder repo clean'
$COMMAND repo clean || enable_connection_exit
print_single_separator
echo 'TEST: clowder repo commit'
pushd .clowder || exit 1
touch newfile || enable_connection_exit
# git add newfile || enable_connection_exit
popd || exit 1
$COMMAND repo add newfile || enable_connection_exit
$COMMAND repo commit 'Add newfile' || enable_connection_exit
pushd .clowder || exit 1
git reset --hard HEAD~1 || enable_connection_exit
popd || exit 1
print_single_separator
echo 'TEST: clowder repo pull'
$COMMAND repo pull && enable_connection_exit
print_single_separator
echo 'TEST: clowder repo push'
$COMMAND repo push && enable_connection_exit
print_single_separator
echo 'TEST: clowder repo run'
$COMMAND repo run 'git status' || enable_connection_exit
print_single_separator
# echo 'TEST: clowder repo status'
# $COMMAND repo status || enable_connection_exit
# print_single_separator
echo 'TEST: clowder save'
$COMMAND save offline_version || enable_connection_exit
print_single_separator
echo 'TEST: clowder start'
$COMMAND start local_branch || enable_connection_exit
for project in "${all_projects[@]}"; do
    pushd $project || exit 1
    test_branch 'local_branch'
    popd || exit 1
done
print_single_separator
echo 'TEST: clowder start -t'
$COMMAND start -t tracking_branch && enable_connection_exit
print_single_separator
echo 'TEST: clowder stash'
$COMMAND stash || enable_connection_exit
print_single_separator
echo 'TEST: clowder status'
$COMMAND status || enable_connection_exit
print_single_separator
echo 'TEST: clowder status -f'
$COMMAND status -f && enable_connection_exit
print_single_separator
echo 'TEST: clowder sync'
$COMMAND sync && enable_connection_exit
print_single_separator
echo 'TEST: clowder init'
rm -rf .clowder || enable_connection_exit
$COMMAND init git@github.com:JrGoodle/cats.git && enable_connection_exit
print_single_separator

# echo 'You can enable your network connection again'
# echo ''
enable_network_connection
