import re


def camel_to_underscore(name):
    '''
    Convert a name such as `SpamEggs` to `spam_eggs`

    >>> camel_to_underscore('SpamEggs')
    'spam_eggs'
    '''
    def replace(match):
        return '_%s' % match.group(0).lower()

    return re.sub('[A-Z]+', replace, name).lstrip('_')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
