@all @status @cats
Feature: Test clowder status

    @help @success
    Scenario: Test clowder status help in empty directory
        Given test directory is empty
        When I run commands 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @help @success
    Scenario: Test clowder status help with invalid clowder.yaml
        Given cats example is initialized to yaml-validation
        And test-empty-project yaml version is linked
        When I run commands 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @help @success
    Scenario: Test clowder status help with valid clowder.yaml
        Given cats example is initialized
        When I run commands 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @default @success
    Scenario: Test clowder status
        Given cats example is initialized and herded
        And mu has untracked file catnip.txt

        When I run 'clowder status'
        And I run 'clowder status' for project jrgoodle/kishka
        And I run 'clowder status' for projects jrgoodle/mu and jrgoodle/duke
        And I run 'clowder status' for projects jrgoodle/mu, jrgoodle/duke, jrgoodle/kit
        And I run 'clowder status' for group black-cats
        And I run 'clowder status' for groups black-cats and cats
        And I run 'clowder status' for groups black-cats, cats, all

        Then mu has untracked file catnip.txt
#        And TODO: check the output

    @default @success @internet
    Scenario: Test clowder status fetch
        Given cats example is initialized and herded
        And mu has untracked file catnip.txt

        When I run 'clowder status -f'
        And I run 'clowder status -f' for project jrgoodle/kishka
        And I run 'clowder status -f' for projects jrgoodle/mu and jrgoodle/duke
        And I run 'clowder status -f' for projects jrgoodle/mu, jrgoodle/duke, jrgoodle/kit
        And I run 'clowder status -f' for group black-cats
        And I run 'clowder status -f' for groups black-cats and cats
        And I run 'clowder status -f' for groups black-cats, cats, all

        Then mu has untracked file catnip.txt
#        And TODO: check the output
