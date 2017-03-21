sqlite3_model
=============

.. automodule:: egegrouper.sqlite3_model
		
   .. autoclass:: egegrouper.sqlite3_model.Model
   
      .. automethod:: __init__(self)
      .. automethod:: add_exam_from_json_file(self, file_name)
      .. automethod:: add_gs_db(self, file_name)
      .. automethod:: add_sme_db(self, file_name)
      .. automethod:: close_storage(self)
      .. automethod:: create_storage(self, file_name)
      .. automethod:: delete_exam(self, exam_id)
      .. automethod:: delete_group(self, group_id)
      .. automethod:: do_if_storage_opened(method)
      .. automethod:: exam(self, exam_id)
      .. automethod:: export_exam_to_json_file(self, exam_id, file_name)
      .. automethod:: group_exam(self, exam_id, group_ids, placed_in)
      .. automethod:: group_info(self, group_id)
      .. automethod:: group_record(self, group_id)
      .. automethod:: insert_exam(self, e)
      .. automethod:: insert_group(self, name, description)
      .. automethod:: open_storage(self, file_name)
      .. automethod:: storage_exists(self, file_name)
      .. automethod:: storage_info(self)
      .. automethod:: update_group_record(self, group_id, attr)
      .. automethod:: where_exam(self, exam_id)

   .. autoclass:: egegrouper.sqlite3_model.DBImporter
      :members:
		      
   .. autoclass:: egegrouper.sqlite3_model.SMEDBImporter
      :members:
      
   .. autoclass:: egegrouper.sqlite3_model.GSDBImporter
      :members:
