# Visualization programmed in python using 3b1b

I am collecting some of my attempts of using the python library and manimgl (not the community edition!).

All scripts where created on a mac book pro using a conda environment.

```bash
conda activate 3b1b
manimgl start.py Data
```

All movies where generated with:

```bash
manimgl -w start.py Data
```

## Z-stacking issue

One of the first things I tried was a failure. I wanted to show how data is produced by a DVD writer. The writer is a box, the DVD are two circles, sounds very straight forward. Issue with z-stacking comes up when you take the 'DVD out of the drive'.


<video controls="" width="800" height="500" muted="" loop="" autoplay="">
<source src="https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Anim.mp4" type="video/mp4">
</video>
