import clowder.utilities

class Meow(object):

    def __init__(self):
        command = 'repo status'
        clowder.utilities.ex(command)
