@cats @link
Feature: clowder link command

    @help
    Scenario: link help in empty directory
        Given test directory is empty
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @help
    Scenario: link help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    @help
    Scenario: link help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder link -h' and 'clowder link --help'
        Then the commands succeed

    Scenario: link default version
        Given cats example is initialized
        And linked tags clowder version
        When I run 'clowder link'
        Then the command succeeds
        And default clowder version is linked

    Scenario: link version
        Given cats example is initialized
        And default clowder version is linked
        When I run 'clowder link tags'
        Then the command succeeds
        And tags clowder version is linked

    @subdirectory
    Scenario: link default version subdirectory
        Given cats example is initialized and herded
        And linked tags clowder version
        When I change to directory black-cats/kit
        And I run 'clowder link'
        Then the command succeeds
        And default clowder version is linked

    @subdirectory
    Scenario: link version subdirectory
        Given cats example is initialized and herded
        And default clowder version is linked
        When I change to directory duke
        And I run 'clowder link tags'
        Then the command succeeds
        And tags clowder version is linked

    @fail
    Scenario: link no versions
        Given cats example is initialized
        And clower repo has no saved versions
        And default clowder version is linked
        And .clowder/versions directory doesn't exist
        When I run 'clowder link missing-version'
        Then the command fails
        And default clowder version is linked
        And .clowder/versions directory doesn't exist

    @fail
    Scenario: link missing version
        Given cats example is initialized
        And default clowder version is linked
        When I run 'clowder link missing-version'
        Then the command fails
        And default clowder version is linked

    @fail
    Scenario: link duplicate versions
        Given cats example is initialized
        And has duplicate clowder versions
        And default clowder version is linked
        When I run 'clowder link duplicate-version'
        Then the command fails
        And default clowder version is linked

    Scenario: link file extension yml to yaml
        Given cats example is initialized to branch extension
        And default clowder version is linked
        And clowder.yml symlink exists
        And clowder.yaml symlink doesn't exist
        When I run 'clowder link tags'
        Then the command succeeds
        And tags clowder version is linked
        And clowder.yaml symlink exists
        And clowder.yml symlink doesn't exist

    Scenario: link file extension yaml to yml
        Given cats example is initialized to branch extension
        And linked tags clowder version
        And clowder.yaml symlink exists
        And clowder.yml symlink doesn't exist
        When I run 'clowder link'
        Then the command succeeds
        And default clowder version is linked
        And clowder.yml symlink exists
        And clowder.yaml symlink doesn't exist

    @fail
    Scenario: has duplicate symlinks
        Given cats example is initialized to branch extension
        And default clowder version is linked
        And created clowder.yaml symlink pointing to .clowder/versions/tags.clowder.yaml
        And clowder.yml and clowder.yaml symlinks exist
        When I run 'clowder status'
        Then the command fails
        And default clowder version is linked
        And clowder.yml symlink exists
        And clowder.yaml symlink exists


    Scenario: link with duplicate symlinks
        Given cats example is initialized to branch extension
        And default clowder version is linked
        And created clowder.yaml symlink pointing to .clowder/versions/tags.clowder.yaml
        And clowder.yml and clowder.yaml symlinks exist
        When I run 'clowder link'
        And I run 'clowder status'
        Then the commands succeed
        And default clowder version is linked
        And clowder.yml symlink exists
        And clowder.yaml symlink doesn't exist

    @cats
    Scenario: link existing .clowder symlink
        Given cats example clowder repo symlink exists
        And .clowder is a symlink
        And clowder.yaml and clowder.yml symlinks don't exist
        When I run 'clowder link'
        Then the command succeeds
        And .clowder symlink exists
        And clowder.yml symlink doesn't exist
        And clowder.yaml is a symlink pointing to .clowder/clowder.yaml

    @offline
    Scenario: link default version offline
        Given cats example is initialized
        And linked tags clowder version
        When the network connection is disabled
        And I run 'clowder link'
        And the network connection is enabled
        Then the command succeeds
        And default clowder version is linked

    @offline
    Scenario: link version offline
        Given cats example is initialized
        And default clowder version is linked
        When the network connection is disabled
        And I run 'clowder link tags'
        And the network connection is enabled
        Then the command succeeds
        And tags clowder version is linked
