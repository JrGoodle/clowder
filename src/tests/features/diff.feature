@all @diff @cats
Feature: Test clowder diff

    @default @succeed
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
