# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals
)


class Xmlwriter(object):
    '''This is a description of the class.'''

    #: An example class variable.
    aClassVariable = True

    def __init__(self, argumentName, anOptionalArg=None):
        '''Initialization method.

        Args:
            argumentName (str): The path of the file to wrap
            anOptionalArg (FileStorage): The :class:`FileStorage` instance to
            wrap

        Returns:
            Xmlwriter: New instance of
            :class:`Xmlwriter`
        '''

        self.instanceVariable1 = argumentName

        if anOptionalArg:
            print('anOptionalArg: %s' % anOptionalArg)
