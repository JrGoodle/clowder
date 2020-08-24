@all @diff @cats
Feature: Test clowder diff

    @default @succeed
    Scenario: Test clowder diff
        Given cats example is initialized and herded
        And mu has untracked file catnip.txt

        When I run 'clowder diff'

        Then mu has untracked file catnip.txt
#        And TODO: check the output
