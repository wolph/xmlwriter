import re


def camel_to_underscore(name):
    '''
    Convert a name such as `SpamEggs` to `spam_eggs`

    >>> camel_to_underscore('SpamEggs')
    'spam_eggs'

    >>> camel_to_underscore('spamEggs')
    'spam_eggs'

    >>> camel_to_underscore('Spam_Eggs')
    'spam_eggs'

    >>> camel_to_underscore('SPAMEggs')
    'spam_eggs'
    '''
    def replace(match):
        parts = ['_']
        # Special cases such as XMLElement will be replaced by xml_element as
        # well
        if match.group(1):
            parts.append(match.group(1).lower())
            parts.append('_')

        parts.append(match.group(2).lower())
        return ''.join(parts)

    return re.sub('_*([A-Z]*)([A-Z])', replace, name).lstrip('_')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
