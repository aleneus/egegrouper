controller
==========

.. automodule:: egegrouper.controller
		
   .. autoclass:: egegrouper.controller.Controller

      .. automethod:: __init__(self, model)
      .. automethod:: add_exam_from_json_file(self, file_name)
      .. automethod:: add_gs_db(self, file_name)
      .. automethod:: add_sme_db(self, file_name)
      .. automethod:: close_storage(self)
      .. automethod:: create_storage(self, file_name)
      .. automethod:: create_storage(self, file_name)
      .. automethod:: delete_exam(self, exam_id)
      .. automethod:: delete_group(self, group_id)
      .. automethod:: exam(self, exam_id)
      .. automethod:: export_exam_to_json_file(self, exam_id, file_name)
      .. automethod:: group_exam(self, exam_id, group_ids, placed_in)
      .. automethod:: group_info(self, group_id)
      .. automethod:: group_record(self, group_id)
      .. automethod:: insert_group(self, name, description)
      .. automethod:: merge_exams(self, exam_id_1, exam_id_2)
      .. automethod:: model_can_grumble(method)
      .. automethod:: model_can_grumble(method)
      .. automethod:: open_or_create_storage(self, file_name)
      .. automethod:: open_or_create_storage(self, file_name)
      .. automethod:: open_storage(self, file_name)
      .. automethod:: plot_exam(self, exam_id)
      .. automethod:: set_view_exam(self, view)
      .. automethod:: set_view_exam_plot(self, view)
      .. automethod:: set_view_group(self, view)
      .. automethod:: set_view_message(self, view)
      .. automethod:: set_view_storage(self, view)
      .. automethod:: set_view_where_exam(self, view)
      .. automethod:: show_message(self, text)
      .. automethod:: show_message(self, text)
      .. automethod:: storage_info(self)
      .. automethod:: update_group_record(self, group_id, attr)
      .. automethod:: where_exam(self, exam_id)
		      
