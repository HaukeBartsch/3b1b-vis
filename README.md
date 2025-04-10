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

One of the first things I tried was a failure. I wanted to show how data is produced by a DVD writer. The writer is a square, the DVD is represented by two circles. An issue with z-stacking comes up when you take the 'DVD out of the drive'.

![DVD](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Anim.gif)

When animated on its own instead of staying 'behind' the square the circles immediately jump in front of the square. Here is the code (start.py/Anim):

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

This seems to be related z_index to be restricted to a positive integer? Changing the z-value you can also see that the camera is a 3D perspective camera. Objects change in apparent size of they have higher z-values.

## Outliers in a probability function

In the second attempt of using the python library 3b1b I tried to visualize an outlier in a distribution in order to show how likely it would be to get such a value. Sounds more complex? Yes, it was.

![DVD](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/ProbOutlier.gif)


```python
class ProbOutlier(Scene):
    def construct(self):
        alpha_tracker = ValueTracker(0.0)
        axes_start = Axes((-5, 25, 5), (0,3), height= FRAME_HEIGHT - 2, width = FRAME_WIDTH - 0.4)
        y_label = axes_start.get_y_axis_label('\\text{observations}', buff=0.6, direction=RIGHT, edge=UP)
        gauss_start_graph = axes_start.get_graph(
            lambda x: alpha_tracker.get_value() * (np.exp(-0.1*(x+3-10)**2)+np.exp(-0.1*(x-3-10)**2)+np.exp(-0.05*(x-0.1-10)**2)+np.exp(-0.05*(x+0.1-10)**2)), 
            color=BLUE
        )
        gauss_start_label = axes_start.get_graph_label(gauss_start_graph, label='V')

        self.wait(2)
        self.play(
            FadeIn(y_label),
            Write(axes_start, lag_ratio=0.01, run_time=1))
        #self.wait()
        self.play(
            #FadeOut(y_label),
            ShowCreation(gauss_start_graph),
            FadeIn(gauss_start_label, RIGHT),
        )
        self.wait()

        def func_all(x):
            return alpha_tracker.get_value() * (np.exp(-0.1*(x+3-10)**2)+np.exp(-0.1*(x-3-10)**2)+np.exp(-0.05*(x-0.1-10)**2)+np.exp(-0.05*(x+0.1-10)**2))

        gauss_start_graph.add_updater(
            lambda x: x.become(
                axes_start.get_graph(
                    lambda x: func_all(x),
                    color=BLUE
                )
            )
        )
        self.play(alpha_tracker.animate.set_value(1.0), run_time=3)

        def func_partial(x, up_to):
            if x > up_to:
                return 0
            return func_all(x)

        # plot a point with a line along the y-axis
        x_of_dot = ValueTracker(0.0)
        point = Dot(axes_start.coords_to_point(10, 0), color=RED)
        point.add_updater(
            lambda x: x.move_to(axes_start.coords_to_point(x_of_dot.get_value(), func_all(x_of_dot.get_value())))
        )
        self.add(point)

        partial_gauss_start_graph = axes_start.get_graph(
            lambda x: func_partial(x, x_of_dot.get_value()), 
            color=ORANGE,
            discontinuities=[x_of_dot.get_value()],
            use_smoothing=False
        )
        partial_gauss_start_graph.add_updater(
            lambda x: x.become(
                axes_start.get_graph(
                    lambda x: func_partial(x, x_of_dot.get_value()), 
                    color=ORANGE,
                    discontinuities=[x_of_dot.get_value()],
                    use_smoothing=False
                )
            )
        )
        # seems like we need a polygon made up of the points in partial_gauss_start_graph to see the area under the curve
        x_vals = np.arange(-1, x_of_dot.get_value(), 0.01)
        c1_points = [
            partial_gauss_start_graph.get_point_from_function(x) for x in x_vals
        ]
        new_point_coord = axes_start.coords_to_point(x_of_dot.get_value(), 0)
        new_point = np.zeros((1, 3))
        new_point[0][0] = new_point_coord[0]
        new_point[0][1] = new_point_coord[1]
        c1_points = np.append(c1_points, new_point, axis=0)

        # get a polygon from the points under the curve
        def getPointsForRegion(v):
            x_vals = np.arange(-1, v, 0.01)
            c1_points = [
                partial_gauss_start_graph.get_point_from_function(x) for x in x_vals
            ]
            new_point_coord = axes_start.coords_to_point(x_of_dot.get_value(), 0)
            new_point = np.zeros((1, 3))
            new_point[0][0] = new_point_coord[0]
            new_point[0][1] = new_point_coord[1]
            c1_points = np.append(c1_points, new_point, axis=0)
            return c1_points

        ps = getPointsForRegion(x_of_dot.get_value())
        region = Polygon(
            *ps,
            stroke_width=0,
            fill_color=ORANGE,
            fill_opacity=0.5
        )
        self.add(region)
        # update the region under the curve
        region.add_updater(
            lambda x: x.become(
                Polygon(
                    *getPointsForRegion(x_of_dot.get_value()),
                    stroke_width=0,
                    fill_color=ORANGE,
                    fill_opacity=0.5
                )
            )
        )

        self.play(ShowCreation(partial_gauss_start_graph))

        self.wait()
        self.play(x_of_dot.animate.set_value(5), run_time=3)
        self.wait()

```