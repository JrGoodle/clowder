import utilities

class Meow(object):

    def __init__(self, clowder):
        command = 'repo status'
        utilities.ex(command)
