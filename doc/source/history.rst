0.5
===
* Method extract_exams added to base model and implemented in sqlite3 model. It is useful for extraction examinations data from several groups. For example, it can be used to get intersections of groups for ANOVA.

0.4
===

* Import and export parts became more extensible.
* Importers and exporters modules added. All exports and imports removed from model.
* Importers for JSON file, Gastroscan database (converted to sqlite3), SME sqlite3 database implemented.
* Exporter to JSON file implemented.

0.3
===

* Method for extracting full examinations of group added to base_model and sqlite3_model.
* Unit tests for sqlite3_model added.

0.2
===

* The method for setting columns of TableWidget replaced to more flexible one.
* JSON folders replaced to more habituate JSON files. For example, if you export examination you will have the file example.json and the folder example.json.data with signals in text format.
* Unit tests for JSON export and import added.
