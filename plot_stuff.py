from kvwoop import *

kv = KVwoop()

## user variables
songs = 'songs' in sys.argv # to plot songs as vertical lines or not

## different plots
# kv.woop_vs_time('woop_vs_time', songs)
kv.woop_per_song('woop_per_song')
