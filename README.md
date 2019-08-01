# KV Woops analyzer

Two methods are available:

```woop_vs_time```: plot number of woops VS time

```woop_per_song```: a bar chart of number of woops in each song

## Examples

In ```plot_stuff.py```, uncomment the method of choice. Examples of how to run:

```console
python plot_stuff.py
python plot_stuff.py songs
python plot_stuff.py songs save
```

Option "songs" works only for ```woop_vs_time``` and will display the beginnings of tracks as vertical lines. Option "save" works for both plotting methods, and will save the plot as png instead of displaying it
