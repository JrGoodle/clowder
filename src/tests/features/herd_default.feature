Feature: New Syntax
    Run 'clowder init', 'clowder herd', and 'clowder status'

    @herd
    Scenario Outline: Default init
        Given cats example is initialized
        And <directory> doesn't exist

        When I run 'clowder herd'

        Then project at <directory> exists
        And project at <directory> is a git repository
        And project at <directory> is on <branch>
        And project at <directory> is clean

        Examples:
        | directory         | branch |
        | mu                | knead  |
        | duke              | purr   |
        | black-cats/kishka | master |
        | black-cats/kit    | master |
        | black-cats/sasha  | master |
        | black-cats/june   | master |
