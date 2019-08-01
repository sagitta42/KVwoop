import pandas as pd
from myplot import *
import numpy as np

# stupid pandas cannot cycle over colours automatically for vertical lines (bar chart and lines on the plot are OK...)
prop_cycle = plt.rcParams['axes.prop_cycle']
COLORS = prop_cycle.by_key()['color']

class KVwoop(pd.DataFrame):
    def __init__(self):
        # woop info
        table = pd.read_csv('kvwoop.csv')
        table['WoopTime'] = timedelta(table, 'WoopTime') # convert string to time
        table['NumWoops'] = list(range(1, len(table)+1)) # number of woops is index + 1

        pd.DataFrame.__init__(self, table)

        # general track info
        self.info = pd.read_csv('kvalbum.csv')
        self.info['TrackLength'] = timedelta(self.info, 'TrackLength')
        self.info = self.info.set_index('TrackNo', drop=False)
        # add TrackNo info from the general table to the current one to simplify some things later
        self['TrackNo'] = self.SongName.map(dict(zip(self.info['SongName'], self.info['TrackNo'])))
        # self.info = self.info.set_index('SongName', drop=False)


    def woop_vs_time(self, songs=False, save=False):
        '''
        Woop evolution in time. Y axis - cumulative number of woops. Each woop has a label denoting woop type
        Variable songs (True|False) determines whether the track beginnings are marked as vertical dashed lines
        '''

        ## calculate total time throughout songs
        # for all the songs except the first one, it's the track lengths of the previous songs + woop time
        # the first song does not have any woops, so it's just like this:
        for i in range(0, len(self)):
            trackno = self.loc[i]['TrackNo']
            self.at[i, 'TotalTime'] = self.info.loc[:trackno - 1]['TrackLength'].sum() + self.loc[i]['WoopTime']


        # pandas is stupid and doesn't want to plot just timedelta, same as it doesn't want to add timestamps (which actually makes sense ok)
        # convert timedelta to timestamp via creating a random date...
        start = pd.Timestamp('2019-09-13 00:00:00')
        # ...and adding timedeltas to it (which are song durations)
        self['TotalTime'] = start + self['TotalTime']
        # well but now we don't want the date info, only time:
        self['TotalTimeX'] = self['TotalTime'].dt.time

        p = Plot((12,8)) # this is just my pretty plotting framework
        self.plot(x = 'TotalTimeX', y = 'NumWoops', style = '.', ax = p.ax, legend=False, markersize=10, label='_nolabel_', color='k')

        ## annotate
        for i in range(len(self)):
            # the first variables are: text, (x, y), xy being the coordinates of the point (not the text)
            # text coords: what is given in xytext (offset relative to point coords)
            p.ax.annotate(self.loc[i]['WoopType'], (self.loc[i]['TotalTimeX'], self.loc[i]['NumWoops']), fontsize=15, textcoords='offset points', xytext =(-15, 7))#, transform=p.ax.transAxes, fontsize=17)

        ## vertical lines for songs
        # the start of the song is the length of the previous songs (and 0 for the first one)
        self.info.at[1, 'StartTime'] = start# + pd.to_timedelta('00:00:00')
        for i in range(2, len(self.info)+1):
            self.info.at[i, 'StartTime'] = pd.to_datetime(start + self.info.loc[:i-1]['TrackLength'].sum())

        # again, we don't want the full date, only the time on the x axis
        self.info['StartTime'] = self.info['StartTime'].dt.time

        imgname = 'woop_vs_time'

        ## plot track beginnings as vertical lines
        if songs:
            col = 0
            for i in range(1, len(self.info)+1):
                print i
                # print self.info.loc[i]['StartTime']
                # p.ax.axvline(self.info.loc[i]['StartTime'], label='test', linestyle='--', color=COLORS[col])
                p.ax.axvline(self.info.loc[i]['StartTime'], label='(' + str(i) + ') ' + self.info.loc[i]['SongName'], linestyle='--', color=COLORS[col % len(COLORS)])
                col+=1

            p.legend(out=True, ncol=3) # legend only needed if songs are marked
            imgname += '_songs'

        ## prettification
        plt.ylabel('Cumulative number of woops')
        plt.xlabel('Total time')
        p.fig.autofmt_xdate()
        p.pretty(large=0)

        if save:
            plt.savefig(imgname + '.png')
        else:
            plt.show()




    def woop_per_song(self, save):
        ''' Bar chart of number of woops per song in decreasing order '''

        toplot = self.groupby('SongName').size()
        toplot = toplot.sort_values(ascending=False)

        p = Plot((10,8))
        toplot.plot.bar()
        plt.xlabel('Song')
        plt.ylabel('Number of woops')
        p.pretty()

        if save:
            plt.savefig('woop_per_song.png')
        else:
            plt.show()



# helper function
def timedelta(df, cname):
    '''
    df: dataframe, cname: column name
    Convert string "MM:SS" to timedelta format in order to be able to add times later
    '''

    ## time format HH:MM:SS
    return pd.to_timedelta('00:' + df[cname].map(str))
