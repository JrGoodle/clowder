@status @cats
Feature: clowder status

    @help @success
    Scenario: clowder status help in empty directory
        Given test directory is empty
        When I run 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @help @success
    Scenario: clowder status help with invalid clowder.yaml
        # https://github.com/JrGoodle/cats/blob/master/versions/yaml-validation.clowder.yaml
        Given cats example is initialized to branch yaml-validation
        And did link test-empty-project clowder version
        When I run 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @help @success
    Scenario: clowder status help with valid clowder.yaml
        Given cats example is initialized
        When I run 'clowder status -h' and 'clowder status --help'
        Then the commands succeed

    @success
    Scenario: clowder status
        Given cats example is initialized and herded
        And mu has untracked file catnip.txt
        When I run 'clowder status'
        And I run 'clowder status jrgoodle/kishka'
        And I run 'clowder status jrgoodle/mu jrgoodle/duke'
        And I run 'clowder status jrgoodle/mu jrgoodle/duke jrgoodle/kit'
        And I run 'clowder status black-cats'
        And I run 'clowder status black-cats cats'
        And I run 'clowder status black-cats cats all'
        Then the commands succeed
        And mu has untracked file catnip.txt
#        And TODO: check the output

    @success @internet
    Scenario: clowder status with fetch
        Given cats example is initialized and herded
        And mu has untracked file catnip.txt
        When I run 'clowder status -f'
        And I run 'clowder status -f jrgoodle/kishka'
        And I run 'clowder status -f jrgoodle/mu jrgoodle/duke'
        And I run 'clowder status -f jrgoodle/mu jrgoodle/duke jrgoodle/kit'
        And I run 'clowder status -f black-cats'
        And I run 'clowder status -f black-cats cats'
        And I run 'clowder status -f black-cats cats all'
        Then the commands succeed
        And mu has untracked file catnip.txt
#        And TODO: check the output
