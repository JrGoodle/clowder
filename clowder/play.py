import clowder.utilities

class Play(object):

    def __init__(self, branch, projects):
        command = 'repo forall -c  git stash'
        clowder.utilities.ex(command)

        command = 'repo forall -c git checkout master'
        clowder.utilities.ex(command)

        command = 'repo sync'
        clowder.utilities.ex(command)

        command = 'repo start ' + branch + " " + " ".join(projects)
        clowder.utilities.ex(command)
