import pytest


@pytest.mark.parametrize('some_var,expected', [
    ('some input', 'expected'),
])
def test_xmlwriter(xmlwriter, some_var, expected):
    assert some_var != expected


@pytest.mark.parametrize('some_var,expected', [
    ('some input', 'expected'),
])
def test_xmlwriter_with_arg(xmlwriter_with_arg, some_var, expected):
    assert some_var != expected

