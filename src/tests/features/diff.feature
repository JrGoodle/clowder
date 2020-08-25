@diff @cats
Feature: Test clowder diff

    @help @success
    Scenario: Test clowder diff help in empty directory
        Given test directory is empty
        When I run commands 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    @help @success
    Scenario: Test clowder diff help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project yaml version is linked
        When I run commands 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    @help @success
    Scenario: Test clowder diff help with valid clowder.yaml
        Given cats example is initialized
        When I run commands 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    @default @success
    Scenario: Test clowder diff
        Given cats example is initialized and herded
        And mu has untracked file catnip.txt

        When I run 'clowder diff'
        And I run 'clowder diff' for project jrgoodle/kishka
        And I run 'clowder diff' for projects jrgoodle/mu and jrgoodle/duke
        And I run 'clowder diff' for projects jrgoodle/mu, jrgoodle/duke, jrgoodle/kit
        And I run 'clowder diff' for group black-cats
        And I run 'clowder diff' for groups black-cats and cats
        And I run 'clowder diff' for groups black-cats, cats, all

        Then mu has untracked file catnip.txt
#        And TODO: check the output
