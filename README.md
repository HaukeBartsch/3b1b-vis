# Visualization programmed in python using 3b1b

I am collecting some of my attempts of using the python library and manimgl (not the community edition!).

All scripts where created on a mac book pro using a conda environment.

```bash
conda activate 3b1b
manimgl start.py Data
```

All movies where generated with first writing them to disk as mp4 and using ImageMagicks 'convert' to convert them into an animated gif (for display on this page).

```bash
manimgl -w start.py Data
convert videos/Data.mpg videos/Data.gif
```

## Z-stacking issue

One of the first things I tried was a failure. I wanted to show how data is produced by a DVD writer. The writer is a box, the DVD are two circles, sounds very straight forward. Issue with z-stacking comes up when you take the 'DVD out of the drive'.

![DVD](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Anim.gif)

Instead of staying 'behind' the square the circles immediately jump infront of the square. Here is the minimal code (start.py/Anim):

```python
class Anim(Scene):
    def construct(self):
        square = Square()
        square.set_z(1)
        square.set_fill(BLUE, 1)

        circle = Circle()
        circle.set_fill(ORANGE, 1)
        circle.set_stroke(width=0)
        circle.set_z(1)
        circleSmall = circle.copy()
        circleSmall.set_fill(BLACK)
        circleSmall.set_z(1)
        circleSmall.scale(0.2)
        CD = VGroup( circle, circleSmall )

        self.play(FadeIn(square))
        #self.wait()
        self.play(VGroup(circle, circleSmall, square).animate.shift(2 * LEFT))
        self.wait()
        # square.set_z(2)
        # new location should old location but with shift in x only
        self.play(CD.animate.shift(4 * RIGHT))
        self.wait()
```


