# -*- coding: utf-8 -*-
"""Clowder command line utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os


def fork_project_names(clowder):
    """Return group options

    :param ClowderController clowder: ClowderController instance
    :return: List of fork project names
    :rtype: list[str]
    """

    if clowder:
        return clowder.get_all_fork_project_names()
    return ['']


def get_saved_version_names():
    """Return list of all saved versions

    :return: List of all saved version names
    :rtype: list[str]
    """

    versions_dir = os.path.join(os.getcwd(), '.clowder', 'versions')
    if not os.path.exists(versions_dir):
        return None
    return [v for v in os.listdir(versions_dir) if not v.startswith('.') if v.lower() != 'default']


def group_names(clowder):
    """Return group options

    :param ClowderController clowder: ClowderController instance
    :return: List of group names
    :rtype: list[str]
    """

    if clowder:
        return clowder.get_all_group_names()
    return ''


def options_help_message(options, message):
    """Help message for groups option

    :param list[str] options: List of options
    :param str message: Help message
    :return: Formatted options help message
    :rtype: str
    """

    if options == [''] or options is None:
        return message

    help_message = '''
                   {0}:
                   {1}
                   '''

    return help_message.format(message, ', '.join(options))


def project_names(clowder):
    """Return project options

    :param ClowderController clowder: ClowderController instance
    :return: List of project names
    :rtype: list[str]
    """

    if clowder:
        return clowder.get_all_project_names()
    return ''