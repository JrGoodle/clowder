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
            exit 1
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
            exit 1
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
./init.sh || exit 1
begin_command
$COMMAND herd $PARALLEL || exit 1
end_command

# echo 'Disable your network connection'
# # https://unix.stackexchange.com/a/293941
# read -n 1 -s -r -p "Press any key to continue"
# echo ''
# echo ''
disable_network_connection

print_single_separator
echo 'TEST: clowder branch'
begin_command
$COMMAND branch || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder branch -r'
begin_command
$COMMAND branch -r || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder branch -a'
begin_command
$COMMAND branch -a || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder checkout'
begin_command
$COMMAND checkout branch_name || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder clean'
begin_command
$COMMAND clean || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder diff'
begin_command
$COMMAND diff || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder forall'
begin_command
$COMMAND forall $PARALLEL -c 'git status' || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder herd'
begin_command
$COMMAND herd && enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder link'
begin_command
$COMMAND link v0.1 || enable_connection_exit
end_command
begin_command
$COMMAND link || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder prune'
begin_command
$COMMAND prune branch || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder prune -r'
begin_command
$COMMAND prune -r branch && enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder prune -a'
begin_command
$COMMAND prune -a branch && enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder repo add'
begin_command
$COMMAND repo add . || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder repo checkout'
begin_command
$COMMAND repo checkout repo-test || enable_connection_exit
end_command
begin_command
$COMMAND repo checkout master || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder repo clean'
begin_command
$COMMAND repo clean || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder repo commit'
pushd .clowder || exit 1
touch newfile || enable_connection_exit
# git add newfile || enable_connection_exit
popd || exit 1
begin_command
$COMMAND repo add newfile || enable_connection_exit
end_command
begin_command
$COMMAND repo commit 'Add newfile' || enable_connection_exit
end_command
pushd .clowder || exit 1
git reset --hard HEAD~1 || enable_connection_exit
popd || exit 1
print_single_separator
echo 'TEST: clowder repo pull'
begin_command
$COMMAND repo pull && enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder repo push'
begin_command
$COMMAND repo push && enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder repo run'
begin_command
$COMMAND repo run 'git status' || enable_connection_exit
end_command
print_single_separator
# echo 'TEST: clowder repo status'
# begin_command
# $COMMAND repo status || enable_connection_exit
# end_command
# print_single_separator
echo 'TEST: clowder save'
begin_command
$COMMAND save offline_version || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder start'
begin_command
$COMMAND start local_branch || enable_connection_exit
end_command
for project in "${all_projects[@]}"; do
    pushd $project || exit 1
    test_branch 'local_branch'
    popd || exit 1
done
print_single_separator
echo 'TEST: clowder start -t'
begin_command
$COMMAND start -t tracking_branch && enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder stash'
begin_command
$COMMAND stash || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder status'
begin_command
$COMMAND status || enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder status -f'
begin_command
$COMMAND status -f && enable_connection_exit
end_command
print_single_separator
echo 'TEST: clowder init'
rm -rf .clowder || enable_connection_exit
begin_command
$COMMAND init git@github.com:JrGoodle/cats.git && enable_connection_exit
end_command
print_single_separator

# echo 'You can enable your network connection again'
# echo ''
enable_network_connection
