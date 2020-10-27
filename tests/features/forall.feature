@forall
Feature: clowder forall

# TODO: Add parallel tests

    @help @cats
    Scenario: forall help in empty directory
        Given test directory is empty
        When I run 'clowder forall -h' and 'clowder forall --help'
        Then the commands succeed

    @help @cats
    Scenario: forall help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder forall -h' and 'clowder forall --help'
        Then the commands succeed

    @help @cats
    Scenario: forall help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder forall -h' and 'clowder forall --help'
        Then the commands succeed

    @cats
    Scenario Outline: forall
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall "git checkout -b v0.1"'
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

    @cats @subdirectory
    Scenario Outline: forall subdirectory
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I change to directory black-cats/sasha
        And I run 'clowder forall "git checkout -b v0.1"'
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

    @parallel @cats
    Scenario Outline: forall parallel
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall --jobs 4 "git checkout -b v0.1"'
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

    @cats
    Scenario Outline: forall group
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall "git checkout -b v0.1" black-cats '
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

    @cats
    Scenario Outline: forall projects
        Given cats example is initialized and herded
        And project at <directory> is on <start_branch>
        When I run 'clowder forall "git checkout -b v0.1" JrGoodle/mu JrGoodle/duke '
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

    @cats
    Scenario: forall environment variables
        Given cats example is initialized and herded
        When I run 'clowder forall "if [ $PROJECT_NAME != JrGoodle/kit ]; then exit 1; fi" JrGoodle/kit '
        And I run 'clowder forall "if [ $PROJECT_REMOTE != origin ]; then exit 1; fi" JrGoodle/kit '
        And I run 'clowder forall "if [ $PROJECT_REF != refs/heads/master ]; then exit 1; fi" JrGoodle/kit '
        And I run 'clowder forall "if [ $PROJECT_NAME != JrGoodle/duke ]; then exit 1; fi" JrGoodle/duke'
        And I run 'clowder forall "if [ $PROJECT_REMOTE != origin ]; then exit 1; fi" JrGoodle/duke'
        And I run 'clowder forall "if [ $PROJECT_REF != refs/heads/purr ]; then exit 1; fi" JrGoodle/duke'
        Then the commands succeed

    @fail @cats
    Scenario: forall fail command
        Given cats example is initialized and herded
        When I run 'clowder forall "exit 1"'
        Then the command fails

    @cats
    Scenario: forall ignore errors
        Given cats example is initialized and herded
        When I run 'clowder forall -i "exit 1"'
        And I run 'clowder forall --ignore-error "exit 1"'
        Then the commands succeed

    @fail @cats
    Scenario: forall return code
        Given cats example is initialized and herded
        When I run 'clowder forall "exit 42"'
        Then the command exited with return code 42

    @cats
    Scenario: forall script
        Given cats example is initialized and herded
        And forall test scripts were copied to the project directories
        When I run 'clowder forall "./test_forall.sh"'
        And I run 'clowder forall "./test_forall_args.sh one two"'
        And I run 'clowder forall -i "./test_forall_args.sh one"'
        And I run 'clowder forall "./test_forall.sh" black-cats'
        And I run 'clowder forall -i "./test_forall_error.sh"'
        Then the commands succeed

    @fail @cats
    Scenario: forall script fail
        Given cats example is initialized and herded
        And forall test scripts were copied to the project directories
        When I run 'clowder forall "./test_forall_args.sh one"'
        And I run 'clowder forall "./test_forall_error.sh"'
        Then the commands fail

    @cats
    Scenario: forall script environment
        Given cats example is initialized and herded
        And forall test scripts were copied to the project directories
        When I run 'clowder forall "./test_forall_env_kit.sh" JrGoodle/kit'
        And I run 'clowder forall "./test_forall_env_duke.sh" JrGoodle/duke'
        Then the commands succeed

    @cats @subdirectory
    Scenario: forall script environment subdirectory
        Given cats example is initialized and herded
        And forall test scripts were copied to the project directories
        When I change to directory mu
        And I run 'clowder forall "./test_forall_env_kit.sh" JrGoodle/kit '
        And I run 'clowder forall "./test_forall_env_duke.sh" JrGoodle/duke '
        Then the commands succeed

    @fail @cats
    Scenario: forall with failing script
        Given cats example is initialized and herded
        And forall test scripts were copied to the project directories
        When I run 'clowder forall "./test_forall_env_kit.sh"'
        And I run 'clowder forall "./test_forall_env_duke.sh"'
        Then the commands fail

    @cats
    Scenario: forall failing script with ignore errors
        Given cats example is initialized and herded
        And forall test scripts were copied to the project directories
        When I run 'clowder forall -i "./test_forall_env_kit.sh"'
        When I run 'clowder forall -i "./test_forall_env_duke.sh"'
        And I run 'clowder forall --ignore-error "./test_forall_env_kit.sh"'
        And I run 'clowder forall --ignore-error "./test_forall_env_duke.sh"'
        Then the commands succeed

    @misc @upstream
    Scenario: forall script environment upstream
        Given misc example is initialized and herded with https
        And forall test scripts were copied to the project directories
        When I run 'clowder forall "./test_forall_env_upstream.sh" gyp'
        Then the command succeeds

    @fail @misc @upstream
    Scenario: forall script fail environment upstream
        Given misc example is initialized and herded with https
        And forall test scripts were copied to the project directories
        When I run 'clowder forall "./test_forall_env_upstream.sh" djinni'
        Then the command fails

    @misc @upstream
    Scenario: forall environment variables upstream
        Given misc example is initialized and herded with https
        When I run 'clowder forall "if [ $PROJECT_NAME != JrGoodle/gyp ]; then exit 1; fi" gyp'
        And I run 'clowder forall "if [ $PROJECT_REMOTE != origin ]; then exit 1; fi" gyp'
        And I run 'clowder forall "if [ $PROJECT_REF != refs/heads/fork-branch ]; then exit 1; fi" gyp'
        And I run 'clowder forall "if [ $UPSTREAM_NAME != external/gyp ]; then exit 1; fi" gyp'
        And I run 'clowder forall "if [ $UPSTREAM_REMOTE != upstream ]; then exit 1; fi" gyp'
        And I run 'clowder forall "if [ $UPSTREAM_REF != refs/heads/master ]; then exit 1; fi" gyp'
        Then the commands succeed

    @cats @offline
    Scenario: forall offline
        Given cats example is initialized and herded
        When the network connection is disabled
        And I run 'clowder forall "git status"'
        And the network connection is enabled
        Then the command succeeds
