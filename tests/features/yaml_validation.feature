@yaml_validation
Feature: clowder yaml validation

#    Scenario Outline: validate project.branch
#        Given cats example is initialized
#        And <directory> doesn't exist
#        When I run 'clowder herd'
#        Then the command succeeds
#        And project at <directory> is a git repository
#        And project at <directory> has tracking <branch>
#        And project at <directory> is on <branch>
#        And project at <directory> is clean
#        And project at <directory> has <remote> with <url>
#
#        Examples:
#        | directory | branch | remote | url                                                              |
#        | felidae   | felid  | origin | git@polka-dot-cat.git.beanstalkapp.com:polka-dot-cat/felidae.git |
#        | felidae   | felid  | origin | git@github.com:JrGoodle/felidae.git                              |


    Scenario Outline: validate project.branch
        Given <project_property> validation clowders are initialized
        And for validation clowders: <directory> doesn't exist
        When I run 'clowder herd' for validation clowders
        Then the validation commands succeed
        And for validation clowders: project at <directory> is a git repository
        And for validation clowders: project at <directory> has tracking <branch>
        And for validation clowders: project at <directory> is on <branch>

        Examples:
        | project_property | directory | branch |
        | branch           | felidae   | felid  |

