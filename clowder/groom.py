import clowder.utilities

class Groom(object):

    def __init__(self):
        command = 'repo forall -c git fetch --all --prune'
        clowder.utilities.ex(command)
