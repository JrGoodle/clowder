@cats @save
Feature: clowder save command

    @help
    Scenario: save help in empty directory
        Given test directory is empty
        When I run 'clowder save -h' and 'clowder save --help'
        Then the commands succeed

    @help
    Scenario: save help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder save -h' and 'clowder save --help'
        Then the commands succeed

    @help
    Scenario: save help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder save -h' and 'clowder save --help'
        Then the commands succeed

    @fail
    Scenario: save with missing directories
        Given cats example is initialized
        When I run 'clowder save my-new-version'
        Then the command fails

    @fail
    Scenario: save existing version
        Given cats example is initialized and herded
        And tags clowder version exists
        When I run 'clowder save tags'
        Then the command fails

    @fail
    Scenario: save default version
        Given cats example is initialized and herded
        And default clowder version doesn't exist
        When I run 'clowder save default'
        And I run 'clowder save DEFAULT'
        Then the commands fail

    Scenario: save new version with no existing versions directory
        Given cats example is initialized and herded
        And clower repo has no saved versions
        And default clowder version is linked
        And my-new-version clowder version doesn't exist
        And .clowder/versions directory doesn't exist
        When I run 'clowder save my-new-version'
        Then the command succeeds
        And .clowder/versions directory exists
        And my-new-version clowder version exists
        And default clowder version is linked

    Scenario: save new version with existing versions directory
        Given cats example is initialized and herded
        And default clowder version is linked
        And .clowder/versions directory exists
        And my-new-version clowder version doesn't exist
        When I run 'clowder save my-new-version'
        Then the command succeeds
        And my-new-version clowder version exists
        And default clowder version is linked

    @subdirectory
    Scenario: save from subdirectory new version with no existing versions directory
        Given cats example is initialized and herded
        And clower repo has no saved versions
        And default clowder version is linked
        And .clowder/versions directory doesn't exist
        And my-new-version clowder version doesn't exist
        When I change to directory black-cats/june
        And I run 'clowder save my-new-version'
        Then the command succeeds
        And .clowder/versions directory exists
        And my-new-version clowder version exists
        And default clowder version is linked

    @subdirectory
    Scenario: save from subdirectory new version with existing versions directory
        Given cats example is initialized and herded
        And default clowder version is linked
        And .clowder/versions directory exists
        And my-new-version clowder version doesn't exist
        When I change to directory black-cats/june
        And I run 'clowder save my-new-version'
        Then the command succeeds
        And my-new-version clowder version exists
        And default clowder version is linked

    # FIXME: Should probably only allow [A-Za-z0-9-_]+
    Scenario: save new version with path separator in name
        Given cats example is initialized and herded
        And default clowder version is linked
        And my-new-version clowder version doesn't exist
        When I run 'clowder save my/new/version'
        Then the command succeeds
        And my-new-version clowder version exists
        And default clowder version is linked

    @offline
    Scenario: save new version offline
        Given cats example is initialized and herded
        And default clowder version is linked
        And my-new-version clowder version doesn't exist
        When the network connection is disabled
        And I run 'clowder save my-new-version'
        And the network connection is enabled
        Then the command succeeds
        And my-new-version clowder version exists
        And default clowder version is linked
