igrouper example
================

1. Start igrouper

   .. code-block:: console

      $ igrouper example.sme.sqlite 

      EGEGrouper Copyright (C) 2017 Aleksandr Popov

      This program comes with ABSOLUTELY NO WARRANTY; for details type `w'.
      This is free software, and you are welcome to redistribute it
      under certain conditions; type `c' for details.
    

      |   group_id | name    | description   |   number |
      |------------+---------+---------------+----------|
      |          1 | Group 1 |               |        2 |
      |          2 | Group 2 | Test group    |        1 |
      |          0 |         | Ungrouped     |        1 |

      igrouper> 

2. Get help

   .. code-block:: console
   
      igrouper> help

      Documented commands (type help <topic>):
      ========================================
      add_group  add_sme       delete_exam        edit_group   group_info   plot_exam
      add_gs     add_to_group  delete_from_group  exam_info    help         quit     
      add_json   db_info       delete_group       export_json  merge_exams  where_is 

   .. code-block:: console

      igrouper> help plot_exam
      plot_exam id
        
      Plot signals of examination.

      Aliases: p
		   
   **Note:** Many commands have short aliases.
      
3. Show examinations of group 1

   .. code-block:: console

      igrouper> g 1

      |   exam_id | name   | diagnosis   |   age | gender   |
      |-----------+--------+-------------+-------+----------|
      |         1 | Anonym | Healphy     |    21 | m        |
      |         2 | Anonym | Healphy     |    31 | m        |

      igrouper> group_info 1

      |   exam_id | name   | diagnosis   |   age | gender   |
      |-----------+--------+-------------+-------+----------|
      |         1 | Anonym | Healphy     |    21 | m        |
      |         2 | Anonym | Healphy     |    31 | m        |

4. Show measurements of examination

   .. code-block:: console

      igrouper> e 1

      E: Anonym m 21 Healphy
          M: 10/03/2014 11:14:56
          M: 10/03/2014 12:10:45

5. Where is examination?

   .. code-block:: console

      igrouper> we 1

      |    |   group_id | name    |
      |----+------------+---------|
      | X  |          1 | Group 1 |
      |    |          2 | Group 2 |

      igrouper> where_is 2

      |    |   group_id | name    |
      |----+------------+---------|
      | X  |          1 | Group 1 |
      | X  |          2 | Group 2 |

6. Edit group and show groups.

   .. code-block:: console
	 
      igrouper> edit_group 2
      name: Group 2
      description: Test 
      igrouper> d

      |   group_id | name    | description   |   number |
      |------------+---------+---------------+----------|
      |          1 | Group 1 |               |        2 |
      |          2 | Group 2 | Test          |        1 |
      |          0 |         | Ungrouped     |        1 |

7. Quit.

   .. code-block:: console
		
      igrouper> quit
      $
