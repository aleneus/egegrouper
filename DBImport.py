import sqlite3

class DBImporter:
    def DBimport(self, dest_filename, source_filename):
        """
        Import data.
        """	
        self._source_filename = source_filename
        self._dest_filename = dest_filename
        self.run()

class SMEDBImporter(DBImporter):
    def run(self):
        self._dconn = sqlite3.connect(self._dest_filename)
        self._sconn = sqlite3.connect(self._source_filename)
        
        self._dest_c = self._dconn.cursor()
        self._src_c = self._sconn.cursor()
        self._dest_c.execute("attach database ? as 'source';", (self._source_filename,))
        script = open('SMEDBImporter.sql', 'r').read()
        self._dest_c.executescript(script)
        self._dest_c.execute("detach database source;")
        self._dest_c.execute('drop table variable;')
        self._dconn.commit()
        
        self._sconn.close()
        self._dconn.close()
