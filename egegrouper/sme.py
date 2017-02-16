"""Very simple implementation of SME model."""

import json
import numpy as np

class Signal:
    """Signal."""
    
    dt = None
    """Sample step."""
    x = []
    """Samples values."""
    
class Measurement:
    """Measurement."""

    time = None
    """Measurement start time."""
    ss = []
    """Signals."""
    
class Examination:
    """Examination."""
    
    name = None
    """Name of patient."""
    
    age = None
    """Age of patient."""
    
    gender = None
    """Gender of patient."""
    
    diagnosis = None
    """Diagnosis."""
    
    ms = []
    """Measurements."""
    
def merge_exams(e1, e2):
    """Merge exams."""
    e = Examination()
    e = e1
    for m in e2.ms:
        e1.ms.append(m)
    return e
