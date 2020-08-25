@all @status @cats
Feature: Test clowder status

    @default @succeed
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

    @default @succeed @internet
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
