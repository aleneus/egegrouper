import matplotlib.pyplot as plt
from egegrouper.views import *

class ViewExamPlot(ViewExam):
    """Plot view to show details of examination."""
    def show_data(self):
        """Plot signals of examination with matplotlib."""
        plt.clf()
        e = self.data
        n = 0
        for m in e.ms:
            for s in m.ss:
                n = n + 1
        i = 0
        for m in e.ms:
            t = m.time
            for s in m.ss:
                i = i + 1
                plt.subplot(n*100 + 10 + i)
                plt.plot(s.x)
                plt.xlim(0,len(s.x))
                plt.grid(True)
                plt.title(t)

        plt.tight_layout()
        plt.show()
