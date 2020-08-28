@cats @save
Feature: clowder save command

    @help @success
    Scenario: clowder save help in empty directory
        Given test directory is empty
        When I run 'clowder save -h' and 'clowder save --help'
        Then the commands succeed

    @help @success
    Scenario: clowder save help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project clowder version is linked
        When I run 'clowder save -h' and 'clowder save --help'
        Then the commands succeed

    @help @success
    Scenario: clowder save help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder save -h' and 'clowder save --help'
        Then the commands succeed

    @default @fail
    Scenario: clowder save with missing directories
        Given cats example is initialized
        When I run 'clowder save my-new-version'
        Then the command fails

    @default @fail
    Scenario: clowder save existing version
        Given cats example is initialized and herded
        And tags clowder version exists
        When I run 'clowder save tags'
        Then the command fails

    @default @fail
    Scenario: clowder save default version
        Given cats example is initialized and herded
        And default clowder version doesn't exist
        When I run 'clowder save default'
        And I run 'clowder save DEFAULT'
        Then the commands fail

    @default @success
    Scenario: clowder save new version with no existing versions directory
        Given cats example is initialized and herded to no-versions
        And default clowder version is linked
        And my-new-version clowder version doesn't exist
        And clowder versions directory doesn't exist
        When I run 'clowder save my-new-version'
        Then the command succeeds
        And clowder versions directory exists
        And clowder version my-new-version exists
        And default clowder version is linked

    @default @success
    Scenario: clowder save new version with existing versions directory
        Given cats example is initialized and herded
        And default clowder version is linked
        And my-new-version clowder version doesn't exist
        When I run 'clowder save my-new-version'
        Then the command succeeds
        And clowder version my-new-version exists
        And default clowder version is linked

    # FIXME: Should probably only allow [A-Za-z0-9-_]+
    @default @success
    Scenario: clowder save new version with path separator in name
        Given cats example is initialized and herded
        And default clowder version is linked
        And my-new-version clowder version doesn't exist
        When I run 'clowder save my/new/version'
        Then the command succeeds
        And clowder version my-new-version exists
        And default clowder version is linked
