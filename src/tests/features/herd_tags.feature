Feature: New Syntax
    Run 'clowder init', 'clowder herd', and 'clowder status'

    Scenario Outline: Default init
        Given cats example is initialized
        And <directory> doesn't exist
        And tags yaml version is linked

        When I run 'clowder herd'

        Then project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <tag>
        And project at <directory> is clean

        Examples:
        | directory         | tag |
        | mu                | test-clowder-yaml-tag |
        | duke              | purr                  |
        | black-cats/kishka | v0.01                 |
        | black-cats/kit    | v0.01                 |
        | black-cats/sasha  | v0.01                 |
        | black-cats/june   | v0.01                 |
