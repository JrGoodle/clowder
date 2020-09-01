@status @cats
Feature: clowder status

    @help @success
    Scenario: status help in empty directory
        Given test directory is empty
        When I run 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    # TODO: Add links for yaml files used in tests
    # https://github.com/JrGoodle/cats/blob/master/versions/yaml-validation.clowder.yaml
    @help @success
    Scenario: status help with invalid clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And linked test-empty-project clowder version
        When I run 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @help @success
    Scenario: status help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @success
    Scenario: status
        Given cats example is initialized and herded
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        When I run 'clowder status'
        And I run 'clowder status jrgoodle/kishka'
        And I run 'clowder status jrgoodle/mu jrgoodle/duke'
        And I run 'clowder status jrgoodle/mu jrgoodle/duke jrgoodle/kit'
        And I run 'clowder status black-cats'
        And I run 'clowder status black-cats cats'
        And I run 'clowder status black-cats cats all'
        Then the commands succeed
        And project at mu has untracked file catnip.txt
#        And TODO: check the output

    @success @internet
    Scenario: status with fetch
        Given cats example is initialized and herded
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        When I run 'clowder status -f'
        And I run 'clowder status -f jrgoodle/kishka'
        And I run 'clowder status -f jrgoodle/mu jrgoodle/duke'
        And I run 'clowder status -f jrgoodle/mu jrgoodle/duke jrgoodle/kit'
        And I run 'clowder status -f black-cats'
        And I run 'clowder status -f black-cats cats'
        And I run 'clowder status -f black-cats cats all'
        Then the commands succeed
        And project at mu has untracked file catnip.txt
#        And TODO: check the output

    @success @offline
    Scenario: status with fetch
        Given cats example is initialized and herded
        And created file catnip.txt in directory mu
        And project at mu has untracked file catnip.txt
        And the network connection is disabled
        When I run 'clowder status -f'
        And I run 'clowder status -f jrgoodle/kishka'
        And I run 'clowder status -f jrgoodle/mu jrgoodle/duke'
        And I run 'clowder status -f jrgoodle/mu jrgoodle/duke jrgoodle/kit'
        And I run 'clowder status -f black-cats'
        And I run 'clowder status -f black-cats cats'
        And I run 'clowder status -f black-cats cats all'
        Then the commands succeed
        And project at mu has untracked file catnip.txt
#        And TODO: check the output
