import matplotlib.pyplot as plt

from pylab import rcParams

from egegrouper_mvc.view import View

class PlotView(View):
    def exam(self, e, ofile):
        n = 0
        for m in e.ms:
            for s in m.ss:
                n = n + 1
                
        i = 0
        for m in e.ms:
            # t = 'source'
            for s in m.ss:
                i = i + 1
                plt.subplot(n*100 + 10 + i)
                # plt.title(t)
                # t = 'edited'
                plt.plot(s.x)
                plt.xlim(0,len(s.x))
                plt.grid(True)

        plt.tight_layout()
        plt.show()
        return "Plot signals"
