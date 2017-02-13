import json
import numpy as np

class Signal:
    def __init__(self):
        self.dt = None
        self.edited = None
        self.x = []

class Measurement:
    def __init__(self):
        self.time = None
        self.ss = []
        
class Examination:
    def __init__(self):
        self.name = None
        self.age = None
        self.gender = None
        self.diagnosis = None
        self.ms = []