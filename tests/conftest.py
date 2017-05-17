import pytest
import logging
from xmlwriter import Xmlwriter


LOG_LEVELS = {
    '0': logging.ERROR,
    '1': logging.WARNING,
    '2': logging.INFO,
    '3': logging.DEBUG,
}


def pytest_configure(config):
    logging.basicConfig(
        level=LOG_LEVELS.get(config.option.verbose, logging.DEBUG))


@pytest.fixture
def xmlwriter():
    return Xmlwriter('arg')


@pytest.fixture
def xmlwriter_with_arg():
    return Xmlwriter('some_arg', 'some other arg')

