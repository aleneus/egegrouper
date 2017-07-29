base_model
==========

.. automodule:: egegrouper.base_model
		
   .. autoclass:: egegrouper.base_model.BaseModel
   
      .. automethod:: __init__(self)
      .. automethod:: close_storage(self)
      .. automethod:: create_storage(self, name)
      .. automethod:: delete_exam(self, exam_id)
      .. automethod:: delete_group(self, group_id)
      .. automethod:: do_if_storage_opened(method)
      .. automethod:: exam(self, exam_id)
      .. automethod:: exams(self, group_id)
      .. automethod:: extract_exams(self, group_ids, operation = 'union')
      .. automethod:: group_exam(self, exam_id, group_ids, placed_in)
      .. automethod:: group_info(self, group_id)
      .. automethod:: group_record(self, group_id)
      .. automethod:: insert_exam(self, e)
      .. automethod:: insert_group(self, name, description)
      .. automethod:: open_or_create_storage(self, name)
      .. automethod:: open_storage(self, name)
      .. automethod:: set_state(self, **kwargs)
      .. automethod:: state(self)
      .. automethod:: storage_exists(self, name)
      .. automethod:: storage_info(self)
      .. automethod:: update_group_record(self, group_id, attr)
      .. automethod:: where_exam(self, exam_id)
