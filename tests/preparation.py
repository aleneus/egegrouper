import os
import shutil
import numpy as np

from egegrouper import sme

def create_test_exam():
    """Create test examination."""
    e = sme.Examination()
    m1 = sme.Measurement()
    s11 = sme.Signal()
    s11.x = np.array([1,2,3,4,5])
    m1.ss = [s11]
    m2 = sme.Measurement()
    s21 = sme.Signal()
    s21.x = np.array([1,2,3,4,5])
    m2.ss = [s21]
    e.ms = [m1, m2]
    return e

def remove_file(file_name):
    abs_file_name = os.path.expanduser(file_name)
    if os.path.isfile(abs_file_name):
        os.remove(abs_file_name)

def remove_folder(dir_name):
    abs_dir_name = os.path.expanduser(dir_name)
    if os.path.isdir(abs_dir_name):
        shutil.rmtree(abs_dir_name)
