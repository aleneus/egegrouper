import matplotlib.pyplot as plt
from egegrouper_mvc.view import View

class ViewPlot(View):
    def exam(self, e):
        n = 0
        for m in e.ms:
            for s in m.ss:
                n = n + 1
                
        i = 0
        #plt.suptitle('{} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis))
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
        return "Plot signals"
