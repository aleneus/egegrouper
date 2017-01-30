import matplotlib.pyplot as plt

from pylab import rcParams
#from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Monospace']})
#rc('text', usetex=True)
#rc('text.latex',unicode=True)
#rc('text.latex',preamble='\\usepackage[utf8]{inputenc}')
#rc('text.latex',preamble='\\usepackage[russian]{babel}')

class PlotView:
    def plot_examination(self, e, ofile):
        n = 0
        for m in e.ms:
            for s in m.ss:
                n = n + 1 
        rcParams['figure.figsize'] = 8, 2.5*n
        plt.figure()
        i = 0
        for m in e.ms:
            t = 'source'
            for s in m.ss:
                i = i + 1
                plt.subplot(n*100 + 10 + i)
                plt.title(t)
                t = 'edited'
                plt.plot(s.x)
                plt.xlim(0,len(s.x))
                plt.grid(True)

        plt.tight_layout()
        plt.savefig(ofile, dpi=200)
