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

What's new in 0.5
-----------------

* Method extract_exams added to base model and implemented in sqlite3 model. It is useful for extraction examinations data from several groups. For example, it can be used to get intersections of groups for ANOVA.
  
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
   sme_mapping
   model
   sqlite3
   controller
   text
   tk
   plot
   igrouper
   tkgrouper
   importers
   exporters
   
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
