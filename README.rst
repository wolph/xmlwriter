=========
XmlWriter
=========


.. image:: https://travis-ci.org/WoLpH/xmlwriter.svg?branch=master
    :alt: XmlWriter test status
    :target: https://travis-ci.org/WoLpH/xmlwriter

.. image:: https://badge.fury.io/py/xmlwriter.svg
    :alt: XmlWriter Pypi version
    :target: https://pypi.python.org/pypi/xmlwriter

.. image:: https://coveralls.io/repos/WoLpH/xmlwriter/badge.svg?branch=master
    :alt: XmlWriter code coverage
    :target: https://coveralls.io/r/WoLpH/xmlwriter?branch=master

.. image:: https://img.shields.io/pypi/pyversions/xmlwriter.svg
    :alt: Supported Python versions
    :target: https://crate.io/packages/xmlwriter?version=latest

``xmlwriter`` - Python XML writer class inspired by the C# XmlWriter and the Django ORM

Links
-----

* Documentation
    - http://xmlwriter.readthedocs.org/en/latest/
* Source
    - https://github.com/WoLpH/xmlwriter
* Bug reports 
    - https://github.com/WoLpH/xmlwriter/issues
* Package homepage
    - https://pypi.python.org/pypi/xmlwriter
* My blog
    - http://wol.ph/

Install
-------

To install the latest release:

.. code-block:: bash

    pip install xmlwriter

Or if `pip` is not available:
    
.. code-block:: bash

    easy_install xmlwriter
   
To install the latest development release:

.. code-block:: bash

    git clone --branch develop https://github.com/WoLpH/xmlwriter.git xmlwriter
    cd ./xmlwriter
    virtualenv .env
    source .env/bin/activate
    pip install -e .

To run the tests you can use the `py.test` command or just run `tox` to test
everything in all supported python versions.

Usage
-----

* TODO

Contributing
------------

Help is greatly appreciated, just please remember to clone the **development**
branch and to run `tox` before creating pull requests.

Travis tests for `flake8` support and test coverage so it's always good to
check those before creating a pull request.

Development branch: https://github.com/WoLpH/xmlwriter/tree/development

Info
----

==============  ==========================================================
Python support  Python 2.7, >= 3.3
Blog            http://wol.ph/
Source          https://github.com/WoLpH/xmlwriter
Documentation   http://xmlwriter.rtfd.org
Changelog       http://xmlwriter.readthedocs.org/en/latest/history.html
API             http://xmlwriter.readthedocs.org/en/latest/modules.html
Issues/roadmap  https://github.com/WoLpH/xmlwriter/issues
Travis          http://travis-ci.org/WoLpH/xmlwriter
Test coverage   https://coveralls.io/r/WoLpH/xmlwriter
Pypi            https://pypi.python.org/pypi/xmlwriter
Ohloh           https://www.ohloh.net/p/xmlwriter
License         `BSD`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/WoLpH/xmlwriter.git
install dev     .. code-block:: bash

                    $ git clone https://github.com/WoLpH/xmlwriter.git xmlwriter
                    $ cd ./xmlwriter
                    $ virtualenv .env
                    $ source .env/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ py.test
==============  ==========================================================

.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _Documentation: http://xmlwriter.readthedocs.org/en/latest/
.. _API: http://xmlwriter.readthedocs.org/en/latest/modules.html
