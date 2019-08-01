''' Class for convenient and pretty plotting '''

import matplotlib
import matplotlib.pyplot as plt

class Plot:
    def __init__(self,figsize,n=1,sharex=True):
        '''
        figsize: [tuple|list] figure size (e.g. (10,8))
        n: [int] number of subplots
        '''
        fig, ax = plt.subplots(n,figsize=figsize, sharex=sharex)
        self.fig = fig
         # convenient if only have one subplot (not ty type axes[0] all the time)
        self.ax = ax
        # array of all our axes; new axes get added here too (e.g. two subplots, one has 2 y axes, means in total 5 axes in the list)
        self.axes = ax if n > 1 else [ax]


    def legend(self, out=False, ncol=1):
        '''
        out: [True|False] If True, draw one legend outside of the plot, else inside (on each subplot)
        ncol: [int] number of columns
        '''

        if out:
            # draw legend at the bottom
            self.axes[-1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), fancybox=True, shadow=False, ncol=ncol,fontsize=15)
            # remove legends from all other subplots
            for ax in self.axes[:-1]:
                legend = ax.legend()
                legend.remove()
        else:
            # draw legend on each axis
            for ax in self.axes:
                ax.legend(ncol=ncol)


    def pretty(self, large=3, grid='major'):
        ''' Increase font size everywhere, add grid lines '''
        ## increase tick sizes (numbers)
        for ax in self.axes:
            for t in ax.get_xaxis().get_ticklabels():
                t.set_fontsize(15 + large)
            for t in ax.get_yaxis().get_ticklabels():
                t.set_fontsize(15 + large)

            ## increase title sizes
            ax.get_xaxis().get_label().set_fontsize(17 + large)
            ax.get_yaxis().get_label().set_fontsize(17 + large)
            ax.title.set_fontsize(20)
            ## increase legend font
            if ax.get_legend():
                for t in ax.get_legend().get_texts():
                    t.set_fontsize(17 + large)

            ## add gridlines
            if grid: ax.grid(linestyle='--',zorder=0, which=grid)

        ## increase fontsize of texts on the figure
        for t in self.fig.get_children():
            if type(t) == matplotlib.text.Text:
                t.set_fontsize(20)

        ## remove white borders around the plot
        self.fig.tight_layout(rect=[0,0,1,0.97])


    def add_axis(self, ax):
        ''' Used in case a plot has two y axes and we create one additionally externally '''
        self.axes.append(ax)
