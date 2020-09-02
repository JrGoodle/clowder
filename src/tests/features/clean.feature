@clean @cats
Feature: clowder clean

    @help
    Scenario: clean help in empty directory
        Given test directory is empty
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    @help
    Scenario: clean help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    @help
    Scenario: clean help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder clean -h' and 'clowder clean --help'
        Then the commands succeed

    @offline
    Scenario: clean offline
        Given cats example is initialized and herded
        And created file something.txt in directory mu
        And project at mu staged file something.txt
        When the network connection is disabled
        And I run 'clowder clean'
        Then the command succeeds
        And something.txt file doesn't exist in directory mu
        And project at mu is clean
