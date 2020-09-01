@diff @cats
Feature: clowder diff

    @help @success
    Scenario: clowder diff help in empty directory
        Given test directory is empty
        When I run 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    @help @success
    Scenario: clowder diff help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    @help @success @multiline
    Scenario: clowder diff help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder diff -h' and 'clowder diff --help'
        # NOTE: This works, but PyCharm can't parse it
#        When I run:
#            clowder diff -h
#            clowder diff --help
        Then the commands succeed

    @success
    Scenario: clowder diff
        Given cats example is initialized and herded
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        When I run 'clowder diff'
        And I run 'clowder diff jrgoodle/kishka'
        And I run 'clowder diff jrgoodle/mu jrgoodle/duke'
        And I run 'clowder diff' jrgoodle/mu jrgoodle/duke jrgoodle/kit'
        And I run 'clowder diff black-cats'
        And I run 'clowder diff black-cats cats'
        And I run 'clowder diff black-cats cats all'
        Then project at mu has untracked file catnip.txt
#        And TODO: check the output

    @success @offline
    Scenario: clowder diff
        Given cats example is initialized and herded
        And the network connection is disabled
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        When I run 'clowder diff'
        And I run 'clowder diff jrgoodle/kishka'
        And I run 'clowder diff jrgoodle/mu jrgoodle/duke'
        And I run 'clowder diff' jrgoodle/mu jrgoodle/duke jrgoodle/kit'
        And I run 'clowder diff black-cats'
        And I run 'clowder diff black-cats cats'
        And I run 'clowder diff black-cats cats all'
        Then project at mu has untracked file catnip.txt
