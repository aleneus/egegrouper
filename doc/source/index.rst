.. egegrouper documentation master file, created by
   sphinx-quickstart on Wed Feb 15 16:04:52 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EGEGrouper documentation!
====================================

Electrogastrography (EGG) and electrogastroenterography (EGEG) are electrophysiological methods for diagnostics of stomach and gastrointestinal tract motility.

This package provides the abilities of forming the sets of EGG and EGEG examinations data for follow statistical processing.

EGEGrouper `repository <https://bitbucket.org/aleneus/egegrouper>`_

Contacts:

* aleneus@gmail.com
* `DSPLab at NArFU <http://dsplab.narfu.ru>`_ (In Russ.)

What's new in 1.0
-----------------

* Architecture in the import and export (TODO) part changed.
* Importers module added.
* Importer for JSON file implemented.
* Importer for Gastroscan sqlite database added. (TODO)    
* Import and adding data from another storage of the same type (merging storages) are different things now.

Requires
--------

* matplotlib
* tabulate
* pyreadline (on Windows)

For users
---------

.. toctree::
   :maxdepth: 1

   installation
   tkgrouper_guide
   igrouper_guide

Modules
-------

.. toctree::
   :maxdepth: 1

   sme
   model
   sqlite3
   controller
   text
   tk
   plot
   igrouper
   tkgrouper
   importers
   
History
-------   
   
.. toctree::
   :maxdepth: 2

   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

