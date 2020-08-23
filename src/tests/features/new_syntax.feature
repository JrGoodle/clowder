Feature: New Syntax
    Run 'clowder init', 'clowder herd', and 'clowder status'

    Scenario: Default init
        Given I'm using the default cats clowder.yml
        And I'm in an empty directory

        When I run 'clowder init git@github.com:JrGoodle/cats.git'
        And I run 'clowder herd'
        And I run 'clowder status'

        Then Project at directory mu is on branch knead
        And Project at directory duke is on branch heads/purr
        And Project at directory black-cats/kishka is on branch master
        And Project at directory black-cats/kit is on branch master
        And Project at directory black-cats/sasha is on branch master
        And Project at directory black-cats/june is on branch master
