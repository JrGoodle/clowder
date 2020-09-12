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

    @debug
    Scenario: validate project.branch
        Given validating property <project_branch>
        And validation clowder is initialized
        And felidae directory doesn't exist
        When I run 'clowder herd'
        Then the command succeeds
        And project at felidae is a git repository
        And project at felidae has tracking branch felid
        And project at felidae is on branch felid
