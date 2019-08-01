from kvwoop import *
import sys

kv = KVwoop()

## user variables
save = 'save' in sys.argv # to save the plot or not
songs = 'songs' in sys.argv # to plot songs as vertical lines or not

## different plots
kv.woop_vs_time(songs, save)
# kv.woop_per_song(save)
