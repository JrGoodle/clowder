@diff @cats
Feature: clowder diff

    @help
    Scenario: diff help in empty directory
        Given test directory is empty
        When I run 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    @help
    Scenario: diff help with invalid clowder.yaml
        Given cats example is initialized
        And has invalid clowder.yml
        When I run 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    @help
    Scenario: diff help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder diff -h' and 'clowder diff --help'
        Then the commands succeed

    Scenario: diff
        Given cats example is initialized and herded
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        When I run 'clowder diff'
        And I run 'clowder diff JrGoodle/kishka'
        And I run 'clowder diff JrGoodle/mu JrGoodle/duke'
        And I run 'clowder diff JrGoodle/mu JrGoodle/duke JrGoodle/kit'
        And I run 'clowder diff black-cats'
        And I run 'clowder diff black-cats cats'
        And I run 'clowder diff black-cats cats all'
        Then the commands succeed
        And project at mu has untracked file catnip.txt
#        And TODO: check the output

    @subdirectory
    Scenario: diff subdirectory
        Given cats example is initialized and herded
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        When I change to directory black-cats/kishka
        And I run 'clowder diff'
        And I run 'clowder diff JrGoodle/kishka'
        And I run 'clowder diff JrGoodle/mu JrGoodle/duke'
        And I run 'clowder diff JrGoodle/mu JrGoodle/duke JrGoodle/kit'
        And I run 'clowder diff black-cats'
        And I run 'clowder diff black-cats cats'
        And I run 'clowder diff black-cats cats all'
        Then the commands succeed
        And project at mu has untracked file catnip.txt
#        And TODO: check the output

    @offline
    Scenario: diff
        Given cats example is initialized and herded
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        When the network connection is disabled
        And I run 'clowder diff'
        And I run 'clowder diff JrGoodle/kishka'
        And I run 'clowder diff JrGoodle/mu JrGoodle/duke'
        And I run 'clowder diff JrGoodle/mu JrGoodle/duke JrGoodle/kit'
        And I run 'clowder diff black-cats'
        And I run 'clowder diff black-cats cats'
        And I run 'clowder diff black-cats cats all'
        And the network connection is enabled
        Then the commands succeed
        And project at mu has untracked file catnip.txt
