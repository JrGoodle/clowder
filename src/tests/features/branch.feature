@all @branch @cats
Feature: Test clowder branch

    @default @succeed @groups
    Scenario: Test clowder branch
        Given cats example is initialized and herded
#        And mu has untracked file catnip.txt

        When I run 'clowder branch'
        And I run 'clowder branch' for project jrgoodle/kishka
        And I run 'clowder branch' for projects jrgoodle/mu and jrgoodle/duke
        And I run 'clowder branch' for projects jrgoodle/mu, jrgoodle/duke, jrgoodle/kit
        And I run 'clowder branch' for group black-cats
        And I run 'clowder branch' for groups black-cats and cats
        And I run 'clowder branch' for groups black-cats, cats, all

        Then the command printed local branches
#        And TODO: check the output

    @default @succeed @internet
    Scenario: Test clowder branch remote
        Given cats example is initialized and herded
#        And mu has untracked file catnip.txt

        When I run 'clowder branch -r'
        And I run 'clowder branch -r' for project jrgoodle/kishka
        And I run 'clowder branch -r' for projects jrgoodle/mu and jrgoodle/duke
        And I run 'clowder branch -r' for projects jrgoodle/mu, jrgoodle/duke, jrgoodle/kit
        And I run 'clowder branch -r' for group black-cats
        And I run 'clowder branch -r' for groups black-cats and cats
        And I run 'clowder branch -r' for groups black-cats, cats, all

        Then the command printed remote branches
#        And TODO: check the output

    @default @succeed @internet
    Scenario: Test clowder branch all
        Given cats example is initialized and herded
#        And mu has untracked file catnip.txt

        When I run 'clowder branch -a'
        And I run 'clowder branch -a' for project jrgoodle/kishka
        And I run 'clowder branch -a' for projects jrgoodle/mu and jrgoodle/duke
        And I run 'clowder branch -a' for projects jrgoodle/mu, jrgoodle/duke, jrgoodle/kit
        And I run 'clowder branch -a' for group black-cats
        And I run 'clowder branch -a' for groups black-cats and cats
        And I run 'clowder branch -a' for groups black-cats, cats, all

        Then the command printed all branches
#        And TODO: check the output
