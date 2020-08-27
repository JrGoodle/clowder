@forall
Feature: clowder forall

    @help @success @cats
    Scenario: clowder forall help in empty directory
        Given test directory is empty
        When I run 'clowder forall -h' and 'clowder forall --help'
        Then the commands succeed

    @help @success @cats
    Scenario: clowder forall help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project yaml version is linked
        When I run 'clowder forall -h' and 'clowder forall --help'
        Then the commands succeed

    @help @success @cats
    Scenario: clowder forall help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder forall -h' and 'clowder forall --help'
        Then the commands succeed

    @default @success @cats
    Scenario Outline: clowder forall
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall -c "git checkout -b v0.1"'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch |
        | mu                | knead        | v0.1       |
        | duke              | purr         | v0.1       |
        | black-cats/kishka | master       | v0.1       |
        | black-cats/kit    | master       | v0.1       |
        | black-cats/sasha  | master       | v0.1       |
        | black-cats/june   | master       | v0.1       |

    @default @success @parallel @cats
    Scenario Outline: clowder forall parallel
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall --jobs 4 -c "git checkout -b v0.1"'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch |
        | mu                | knead        | v0.1       |
        | duke              | purr         | v0.1       |
        | black-cats/kishka | master       | v0.1       |
        | black-cats/kit    | master       | v0.1       |
        | black-cats/sasha  | master       | v0.1       |
        | black-cats/june   | master       | v0.1       |

    @default @success @cats
    Scenario Outline: clowder forall group
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall black-cats -c "git checkout -b v0.1"'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch |
        | mu                | knead        | knead      |
        | duke              | purr         | purr       |
        | black-cats/kishka | master       | v0.1       |
        | black-cats/kit    | master       | v0.1       |
        | black-cats/sasha  | master       | v0.1       |
        | black-cats/june   | master       | v0.1       |

    @default @success @cats
    Scenario Outline: clowder forall projects
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall jrgoodle/mu jrgoodle/duke -c "git checkout -b v0.1"'
        Then the command succeeds
        And project at <directory> is on <end_branch>

        Examples:
        | directory         | start_branch | end_branch |
        | mu                | knead        | v0.1       |
        | duke              | purr         | v0.1       |
        | black-cats/kishka | master       | master     |
        | black-cats/kit    | master       | master     |
        | black-cats/sasha  | master       | master     |
        | black-cats/june   | master       | master     |

    @default @success @cats
    Scenario: clowder forall environment variables
        Given cats example is initialized and herded
        When I run 'clowder forall jrgoodle/kit -c "if [ $PROJECT_NAME != jrgoodle/kit ]; then exit 1; fi"'
        And I run 'clowder forall jrgoodle/kit -c "if [ $PROJECT_REMOTE != origin ]; then exit 1; fi"'
        And I run 'clowder forall jrgoodle/kit -c "if [ $PROJECT_REF != refs/heads/master ]; then exit 1; fi"'
        And I run 'clowder forall jrgoodle/duke -c "if [ $PROJECT_NAME != jrgoodle/duke ]; then exit 1; fi"'
        And I run 'clowder forall jrgoodle/duke -c "if [ $PROJECT_REMOTE != origin ]; then exit 1; fi"'
        And I run 'clowder forall jrgoodle/duke -c "if [ $PROJECT_REF != refs/heads/purr ]; then exit 1; fi"'
        Then the commands succeed

    @default @fail @cats
    Scenario: clowder forall fail command
        Given cats example is initialized and herded
        When I run 'clowder forall -c "exit 1"'
        Then the command fails

    @default @success @cats
    Scenario: clowder forall ignore errors
        Given cats example is initialized and herded
        When I run 'clowder forall -ic "exit 1"'
        And I run 'clowder forall --ignore-error -c "exit 1"'
        Then the commands succeed

    @default @fail @cats
    Scenario: clowder forall return code
        Given cats example is initialized and herded
        When I run 'clowder forall -c "exit 42"'
        Then the command exited with return code 42

    @default @success @cats
    Scenario: clowder forall script
        Given cats example is initialized and herded
        And forall test scripts are in the project directories
        When I run 'clowder forall -c "./test_forall.sh"'
        And I run 'clowder forall -c "./test_forall_args.sh" "one" "two"'
        And I run 'clowder forall -ic "./test_forall_args.sh" "one"'
        And I run 'clowder forall black-cats -c "./test_forall.sh"'
        And I run 'clowder forall -ic "./test_forall_error.sh"'
        Then the commands succeed

    @default @fail @cats
    Scenario: clowder forall script fail
        Given cats example is initialized and herded
        And forall test scripts are in the project directories
        When I run 'clowder forall -c "./test_forall_args.sh" "one"'
        And I run 'clowder forall -c "./test_forall_error.sh"'
        Then the commands fail

    @default @success @cats
    Scenario: clowder forall script environment
        Given cats example is initialized and herded
        And forall test scripts are in the project directories
        When I run 'clowder forall jrgoodle/kit -c "./test_forall_env_kit.sh"'
        And I run 'clowder forall jrgoodle/duke -c "./test_forall_env_duke.sh"'
        And I run 'clowder forall jrgoodle/kit -c "./test_forall_env_kit.sh"' from directory mu
        And I run 'clowder forall jrgoodle/duke -c "./test_forall_env_duke.sh"' from directory duke
        And I run 'clowder forall jrgoodle/kit -c "./test_forall_env_kit.sh"' from directory black-cats/june
        And I run 'clowder forall jrgoodle/duke -c "./test_forall_env_duke.sh"' from directory black-cats/sasha
        Then the commands succeed

    @default @fail @cats
    Scenario: clowder forall with failing script
        Given cats example is initialized and herded
        And forall test scripts are in the project directories
        When I run 'clowder forall -c "./test_forall_env_kit.sh"'
        And I run 'clowder forall -c "./test_forall_env_duke.sh"'
        Then the commands fail

    @default @success @cats
    Scenario: clowder forall failing script with ignore errors
        Given cats example is initialized and herded
        And forall test scripts are in the project directories
        When I run 'clowder forall -ic "./test_forall_env_kit.sh"'
        When I run 'clowder forall -ic "./test_forall_env_duke.sh"'
        And I run 'clowder forall --ignore-error -c "./test_forall_env_kit.sh"'
        And I run 'clowder forall --ignore-error -c "./test_forall_env_duke.sh"'
        Then the commands succeed

    @default @success @misc @upstream
    Scenario: clowder forall script environment upstream
        Given misc example is initialized and herded
        And forall test scripts are in the project directories
        When I run 'clowder forall gyp -c "./test_forall_env_upstream.sh"'
        Then the command succeeds

    @default @fail @misc @upstream
    Scenario: clowder forall script fail environment upstream
        Given misc example is initialized and herded
        And forall test scripts are in the project directories
        When I run 'clowder forall djinni -c "./test_forall_env_upstream.sh"'
        Then the command fails

    @default @success @misc @upstream
    Scenario: clowder forall environment variables upstream
        Given misc example is initialized and herded
        When I run 'clowder forall gyp -c "if [ $PROJECT_NAME != JrGoodle/gyp ]; then exit 1; fi"'
        And I run 'clowder forall gyp -c "if [ $PROJECT_REMOTE != origin ]; then exit 1; fi"'
        And I run 'clowder forall gyp -c "if [ $PROJECT_REF != refs/heads/fork-branch ]; then exit 1; fi"'
        And I run 'clowder forall gyp -c "if [ $UPSTREAM_NAME != external/gyp ]; then exit 1; fi"'
        And I run 'clowder forall gyp -c "if [ $UPSTREAM_REMOTE != upstream ]; then exit 1; fi"'
        And I run 'clowder forall gyp -c "if [ $UPSTREAM_REF != refs/heads/master ]; then exit 1; fi"'
        Then the commands succeed
