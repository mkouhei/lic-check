===========
 lic-check
===========

Provides FOSS compatibile licenses when give license to a new project.

Status
======

.. image:: https://secure.travis-ci.org/mkouhei/lic-check.png?branch=master
   :target: http://travis-ci.org/mkouhei/lic-check
.. image:: https://coveralls.io/repos/mkouhei/lic-check/badge.png?branch=master
   :target: https://coveralls.io/r/mkouhei/lic-check?branch=master
.. image:: https://img.shields.io/pypi/v/lic-check.svg
   :target: https://pypi.python.org/pypi/lic-check
.. image:: https://readthedocs.org/projects/lic-check/badge/?version=latest
   :target: https://readthedocs.org/projects/lic-check/?badge=latest
   :alt: Documentation Status


Requirements
============

* Python 2.7 or Python 3.3 over

Features
========

* License classifiers

Setup
=====

::

  $ pip install --user lic-check
  or
  (venv)$ pip install lic-check

Usage
=====

::

  $ python
  >>> from lic_check.classifier import Classifier
  >>> c = Classifier()
  >>> c.segments
  [SoftwareLicenses, DocumentationLicenses, OtherLicenses]
