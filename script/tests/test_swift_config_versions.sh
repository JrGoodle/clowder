#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects example test script'
print_double_separator

if [ -z "$TRAVIS_OS_NAME" ]; then
    setup_local_test_directory
fi

cd "$SWIFT_EXAMPLE_DIR" || exit 1

export project_paths=( 'cmark' \
                       'llbuild' \
                       'swift-corelibs-foundation' \
                       'swift-corelibs-libdispatch' \
                       'swift-corelibs-xctest' \
                       'swift-integration-tests' \
                       'swift-xcode-playground-support' \
                       'swiftpm' )

export llvm_project_paths=( 'clang' \
                            'compiler-rt' \
                            'lldb' \
                            'llvm' )

test_default_branches() {
    echo "TEST: Default branches checked out"
    for project in "${llvm_project_paths[@]}"; do
    	pushd $project
        test_branch stable
        popd
    done
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch master
        popd
    done
    pushd swift
    test_branch master
    popd
    pushd ninja
    test_branch release
    popd
}

test_next_branches() {
    echo "TEST: Version 'next' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
    	pushd $project
        test_branch upstream-with-swift
        popd
    done
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch master
        popd
    done
    pushd swift
    test_branch master-next
    popd
    pushd ninja
    test_branch release
    popd
}

test_swift_3_0_branch_branches() {
    echo "TEST: Version 'swift-3.0-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-3.0-branch'
        popd
    done
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-3.0-branch'
        popd
    done
    pushd swift
    test_branch 'swift-3.0-branch'
    popd
    pushd ninja
    test_branch release
    popd
}

test_swift_3_1_branch_branches() {
    echo "TEST: Version 'swift-3.1-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-3.1-branch'
        popd
    done
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-3.1-branch'
        popd
    done
    pushd swift
    test_branch 'swift-3.1-branch'
    popd
    pushd ninja
    test_branch release
    popd
}

test_swift_4_0_branch_branches() {
    echo "TEST: Version 'swift-4.0-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-4.0-branch'
        popd
    done
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-4.0-branch'
        popd
    done
    pushd swift
    test_branch 'swift-4.0-branch'
    popd
    pushd ninja
    test_branch release
    popd
}

test_swift_4_0_branch_07_11_2017_branches() {
    echo "TEST: Version 'swift-4.0-branch-07-11-2017' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-4.0-branch-07-11-2017'
        popd
    done
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-4.0-branch'
        popd
    done
    pushd swift
    test_branch 'swift-4.0-branch'
    popd
    pushd ninja
    test_branch release
    popd
}

test_swift_4_1_branch_branches() {
    echo "TEST: Version 'swift-4.1-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
    	pushd $project
        test_branch 'swift-4.1-branch'
        popd
    done
    for project in "${project_paths[@]}"; do
    	pushd $project
        test_branch master
        popd
    done
    pushd swift
    test_branch master
    popd
    pushd ninja
    test_branch release
    popd
}

test_init_herd() {
    print_double_separator
    echo "TEST: Normal herd after init"
    ./clean.sh
    ./init.sh  || exit 1
    clowder link -v travis-ci || exit 1
    clowder herd || exit 1
    clowder status || exit 1
}
test_init_herd

export config_versions=( 'next' \
                         'swift-3.0-branch' \
                         'swift-3.1-branch' \
                         'swift-4.0-branch' \
                         'swift-4.0-branch-07-11-2017' \
                         'swift-4.1-branch' )

test_swift_configs() {
    print_double_separator
    echo "TEST: Swift configs"
    for config in "${config_versions[@]}"; do
        config_function="test_${config}_branches"
        config_function="${config_function//-/_}"
        config_function="${config_function//./_}"
	    clowder link -v travis-ci || exit 1
        clowder herd || exit 1
        test_default_branches
        clowder link -v "$config"
        clowder herd || exit 1
        clowder status || exit 1
        "$config_function"
    done
}
test_swift_configs
