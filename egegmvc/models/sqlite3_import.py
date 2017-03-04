import sqlite3
from egegmvc.models import sqlite3_scripts

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
        self._dest_c.executescript(sqlite3_scripts.add_sme_db)
        self._dest_c.execute("detach database source;")
        self._dest_c.execute('drop table variable;')
        self._dconn.commit()
        
        self._sconn.close()
        self._dconn.close()

class GSDBImporter(DBImporter):
    def run(self):
        self._dconn = sqlite3.connect(self._dest_filename)
        self._sconn = sqlite3.connect(self._source_filename)
        
        self._dest_c = self._dconn.cursor()
        self._src_c = self._sconn.cursor()
		
        res = self._src_c.execute('\
        SELECT name, diagnosis, age, sex, date, signal, edited \
        FROM record as r, waveform as w\
        WHERE r.id = w.record_id\
        ')
        
        exam_id, meas_id = self._get_last_ids()
        ind = []
        t = []
        for r in res:
            if self._form_examination(r, t, ind):
                exam_id, meas_id = self._insert_examination(t, ind, exam_id, meas_id)
                t = []
                ind = []
                t.append(r)
                ind.append(1)
        self._insert_examination(t, ind, exam_id, meas_id)
        self._dconn.commit()
        
        self._sconn.close()
        self._dconn.close()
        
    def _get_last_ids(self):
        """
        Get during (last) measurement's and examination's id.
        
        """
        exam_id = list(self._dest_c.execute('SELECT max(exam_id) FROM examination'))[0][0]
        meas_id = list(self._dest_c.execute('SELECT max(meas_id) FROM measurement'))[0][0]
        if not exam_id:
            exam_id = 0
        if not meas_id:
            meas_id = 0
        return (exam_id, meas_id)

    def _insert_examination(self, t, ind, exam_id, meas_id):
        """
        Insert examination to destination DB. Data takes from temprorary lists t and ind.
        
        """
        dt = 0.5
        self._dest_c.execute('\
        INSERT INTO examination (name, diagnosis, age, gender)\
        VALUES (?,?,?,?)',(t[0][0],t[0][1],t[0][2],t[0][3]))
        exam_id += 1
        meas_id += 1
        self._dest_c.execute('\
        INSERT INTO measurement(time, exam_id)\
        VALUES (?,?)',(t[0][4],exam_id))
        self._dest_c.execute('\
        INSERT INTO signal(data, dt, edited,meas_id)\
        VALUES (?,?,?,?)',(t[0][5], dt, t[0][6],meas_id)) 
        if 2 in ind:
            self._dest_c.execute('\
            INSERT INTO signal(data, dt, edited,meas_id)\
            VALUES (?,?,?,?)',(t[ind.index(2)][5], dt, t[ind.index(2)][6],meas_id)) 
        if 3 in ind:
            self._dest_c.execute('\
            INSERT INTO measurement(time, exam_id)\
            VALUES (?,?)',(t[ind.index(3)][4],exam_id))
            meas_id += 1
            self._dest_c.execute('\
            INSERT INTO signal(data, dt, edited, meas_id)\
            VALUES (?,?,?,?)',(t[ind.index(3)][5], dt, t[ind.index(3)][6],meas_id)) 
        if 4 in ind:
            self._dest_c.execute('\
            INSERT INTO signal(data, dt, edited, meas_id)\
            VALUES (?,?,?,?)',(t[ind.index(4)][5], dt, t[ind.index(4)][6],meas_id)) 
        return (exam_id, meas_id)

    def _form_examination(self, r, t, ind):
        """
        Form temprorary lists t and ind.
        
        """
        if len(t) == 0:
            t.append(r)
            ind.append(1)
        else:
            if t[-1][0] == r[0] and t[-1][2] == r[2] and t[-1][3] == r[3] and t[-1][4][:9] == r[4][:9]:
                if ind[-1] == 1 and t[-1][4] == r[4]:
                    ind.append(2)
                elif ind[-1] == 1 or ind[-1] == 2:
                    ind.append(3)
                elif ind[-1] == 3:
                    ind.append(4)
                t.append(r)
                return False
            else:
                return True
