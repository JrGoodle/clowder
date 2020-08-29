@cats @link
Feature: clowder link command

    @help @success
    Scenario: clowder link help in empty directory
        Given test directory is empty
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @help @success
    Scenario: clowder link help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @help @success
    Scenario: clowder link help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @success
    Scenario: clowder link default version
        Given cats example is initialized
        And did link tags clowder version
        When I run 'clowder link'
        Then the command succeeds
        And default clowder version is linked

    @success
    Scenario: clowder link version
        Given cats example is initialized
        And default clowder version is linked
        When I run 'clowder link tags'
        Then the command succeeds
        And tags clowder version is linked

    @fail
    Scenario: clowder link no versions
        Given cats example is initialized to branch no-versions
        And default clowder version is linked
        When I run 'clowder link missing-version'
        Then the command fails
        And default clowder version is linked

    @fail
    Scenario: clowder link missing version
        Given cats example is initialized
        And default clowder version is linked
        When I run 'clowder link missing-version'
        Then the command fails
        And default clowder version is linked

    @fail
    Scenario: clowder link duplicate versions
        Given cats example is initialized to branch duplicate-versions
        And default clowder version is linked
        When I run 'clowder link duplicate-version'
        Then the command fails
        And default clowder version is linked

    @success
    Scenario: clowder link file extension yml to yaml
        Given cats example is initialized to branch extension
        And default clowder version is linked
        And symlink clowder.yml exists
        And symlink clowder.yaml doesn't exist
        When I run 'clowder link tags'
        Then the command succeeds
        And tags clowder version is linked
        And symlink clowder.yaml exists
        And symlink clowder.yml doesn't exist

    @success
    Scenario: clowder link file extension yaml to yml
        Given cats example is initialized to branch extension
        And did link tags clowder version
        And symlink clowder.yaml exists
        And symlink clowder.yml doesn't exist
        When I run 'clowder link'
        Then the command succeeds
        And default clowder version is linked
        And symlink clowder.yml exists
        And symlink clowder.yaml doesn't exist

    @fail
    Scenario: clowder has duplicate symlinks
        Given cats example is initialized to branch extension
        And default clowder version is linked
        And symlink clowder.yaml was created pointing to .clowder/versions/tags.clowder.yaml
        And symlinks clowder.yml and clowder.yaml exist
        When I run 'clowder status'
        Then the command fails
        And default clowder version is linked
        And symlink clowder.yml exists
        And symlink clowder.yaml exists

    @success
    Scenario: clowder link with duplicate symlinks
        Given cats example is initialized to branch extension
        And default clowder version is linked
        And symlink clowder.yaml was created pointing to .clowder/versions/tags.clowder.yaml
        And symlinks clowder.yml and clowder.yaml exist
        When I run 'clowder link'
        And I run 'clowder status'
        Then the commands succeed
        And default clowder version is linked
        And symlink clowder.yml exists
        And symlink clowder.yaml doesn't exist
