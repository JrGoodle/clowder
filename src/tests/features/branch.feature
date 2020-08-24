@all @branch @cats
Feature: Test clowder branch

    @default @succeed @groups
    Scenario: Test clowder branch
        Given cats example is initialized and herded
#        And mu has untracked file catnip.txt

        When I run 'clowder branch' for group black-cats

        Then the command printed local branches
#        And TODO: check the output

    @default @succeed @internet
    Scenario: Test clowder branch remote
        Given cats example is initialized and herded
#        And mu has untracked file catnip.txt

        When I run 'clowder branch -r'

        Then the command printed remote branches
#        And TODO: check the output

    @default @succeed @internet
    Scenario: Test clowder branch all
        Given cats example is initialized and herded
#        And mu has untracked file catnip.txt

        When I run 'clowder branch -a'

        Then the command printed all branches
#        And TODO: check the output
