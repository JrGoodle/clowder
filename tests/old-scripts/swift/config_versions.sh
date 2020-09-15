#!/usr/bin/env bash

# set -xv

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.." || exit 1

. test_utilities.sh

print_double_separator
echo 'TEST: swift projects example test script'
print_double_separator
cd "$SWIFT_EXAMPLE_DIR" || exit 1

export project_paths=( 'swift' \
                       'cmark' \
                       'llbuild' \
                       'swift-tools-support-core' \
                       'swiftpm' \
                       'swift-driver' \
                       'swift-syntax' \
                       'swift-stress-tester' \
                       'swift-corelibs-xctest' \
                       'swift-corelibs-foundation' \
                       'swift-corelibs-libdispatch' \
                       'swift-integration-tests' \
                       'swift-xcode-playground-support' \
                       'indexstore-db' \
                       'sourcekit-lsp' \
                       'swift-format' \
                       'pythonkit' \
                       'tensorflow-swift-apis' )


test_default() {
    echo "TEST: Default branches checked out"
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'master'
        popd || exit 1
    done
    pushd 'swift-argument-parser' || exit 1
    test_tag_commit '0.0.5'
    popd || exit 1
    pushd 'ninja' || exit 1
    test_branch 'release'
    popd || exit 1
    pushd 'yams' || exit 1
    test_tag_commit '3.0.1'
    popd || exit 1
    pushd 'llvm-project' || exit 1
    test_branch 'swift/master'
    popd || exit 1
}

test_default_linux() {
    echo "TEST: Default linux branches checked out"
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'master'
        popd || exit 1
    done
    pushd 'swift-argument-parser' || exit 1
    test_tag_commit '0.0.5'
    popd || exit 1
    pushd 'ninja' || exit 1
    test_branch 'release'
    popd || exit 1
    pushd 'icu' || exit 1
    test_tag_commit 'release-65-1'
    popd || exit 1
    pushd 'yams' || exit 1
    test_tag_commit '3.0.1'
    popd || exit 1
    pushd 'cmake' || exit 1
    test_tag_commit 'v3.16.5'
    popd || exit 1
    pushd 'llvm-project' || exit 1
    test_branch 'swift/master'
    popd || exit 1
}

test_next() {
    echo "TEST: Version 'next' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch upstream-with-swift
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch master
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch master-next
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_3_0_branch() {
    echo "TEST: Version 'swift-3.0-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-3.0-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-3.0-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-3.0-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_3_1_branch() {
    echo "TEST: Version 'swift-3.1-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-3.1-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-3.1-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-3.1-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_4_0_branch() {
    echo "TEST: Version 'swift-4.0-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-4.0-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-4.0-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-4.0-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_4_1_branch() {
    echo "TEST: Version 'swift-4.1-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-4.1-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-4.1-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-4.1-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_4_2_branch() {
    echo "TEST: Version 'swift-4.2-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-4.2-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-4.2-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-4.2-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_5_0_branch() {
    echo "TEST: Version 'swift-5.0-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-5.0-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-5.0-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-5.0-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_5_1_branch() {
    echo "TEST: Version 'swift-5.1-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-5.1-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-5.1-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-5.1-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_swift_5_2_branch() {
    echo "TEST: Version 'swift-5.2-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-5.2-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'swift-5.2-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'swift-5.2-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_release_5_3_branch() {
    echo "TEST: Version 'release-5.3-branch' branches checked out"
    for project in "${llvm_project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'release-5.3-branch'
        popd || exit 1
    done
    for project in "${project_paths[@]}"; do
        pushd $project || exit 1
        test_branch 'release-5.3-branch'
        popd || exit 1
    done
    pushd swift || exit 1
    test_branch 'release-5.3-branch'
    popd || exit 1
    pushd ninja || exit 1
    test_branch release
    popd || exit 1
}

test_init_herd() {
    print_double_separator
    echo "TEST: Normal herd after init"
    ./clean.sh
    ./init.sh  || exit 1
    begin_command
    $COMMAND herd $PARALLEL || exit 1
    end_command
    test_default
    begin_command
    $COMMAND status all linux || exit 1
    end_command
    begin_command
    $COMMAND herd all linux $PARALLEL || exit 1
    end_command
    test_default_linux
    begin_command
    $COMMAND status all linux || exit 1
    end_command
}
test_init_herd

export config_versions=( 'next' \
                         'swift-3.0-branch' \
                         'swift-3.1-branch' \
                         'swift-4.0-branch' \
                         'swift-4.1-branch' \
                         'swift-4.2-branch' \
                         'swift-5.0-branch' \
                         'swift-5.1-branch' \
                         'swift-5.2-branch' \
                         'release-5.3-branch' )

test_swift_configs() {
    print_double_separator
    echo "TEST: Swift configs"
    for config in "${config_versions[@]}"; do
        config_function="test_${config}"
        config_function="${config_function//-/_}"
        config_function="${config_function//./_}"
        begin_command
        $COMMAND link travis-ci || exit 1
        end_command
        begin_command
        $COMMAND herd $PARALLEL || exit 1
        end_command
        test_default
        begin_command
        $COMMAND link "$config" || exit 1
        end_command
        begin_command
        $COMMAND herd $PARALLEL || exit 1
        end_command
        begin_command
        $COMMAND status || exit 1
        end_command
        "$config_function"
        pushd swift || exit 1
            # need to checkout master for latest update-checkout script changes
            # one reason not to include checkout logic in the project repo ;)
            git checkout master || exit 1
        popd || exit 1
        ./swift/utils/update-checkout --clone --scheme master --reset-to-remote || exit 1
        begin_command
        $COMMAND status || exit 1
        end_command
        test_default
        ./swift/utils/update-checkout --scheme "$config" --clone --reset-to-remote || exit 1
        begin_command
        $COMMAND status || exit 1
        end_command
        "$config_function"
    done
}
# test_swift_configs
