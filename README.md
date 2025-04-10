# Visualization in python using 3b1b

I am collecting every attempt of mine using the python library manimlib and manimgl. Scripts are included and the order is basically from the first attempt to most recent.

![From a square to this](https://github.com/HaukeBartsch/3b1b-vis/blob/main/images/LB.png)

All videos where created on a mac-book pro using a conda environment (ManimGL v1.7.2).

```bash
conda activate 3b1b
manimgl start.py Data
```

Movies where generated with manimgl as mp4 and 'convert'-ed (with ImageMagick) to an animated gif (for display on this page).

```bash
manimgl -w start.py Data
convert videos/Data.mpg videos/Data.gif
```

Some gif files where too big so I ommitted them. Watch the corresponding mp4's in the videos folder.

Note that this is only the visual part of a full presentation. I write a script afterwards and use Elevenlabs to create sub-titles. The movie and the sounds files are baked using iMovie.


## Z-stacking

The first things I tried did not work. I wanted to show how data is produced by a DVD writer. The writer is a square and the DVD is represented by two circles. An issue with z-stacking comes up when you 'take the DVD out of the drive'.

![DVD](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Anim.gif)

When the DVD starts to come out of the drive instead of staying 'behind' the square the DVD immediately jump in front of the square.

```python
from manimlib import *

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

Further down in section "DICOM image meta information" I figured out how to do it correctly using "square.z_index = 2" instead of calling the set_z() function.

## Outliers relative to a probability function

In the second attempt of using the python library I tried to visualize an outlier (low probability value) in a distribution. In order to show how the integral to the here left-hand side relates to the likelihood of getting such a value. Sounds more complex? Yes, it was.

![DVD](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/ProbOutlier.gif)

It was a good introduction into the use of value trackers for animations. Problematic was the conversion of the simple function into a closed polygon to be able to 'cut-off' the left-hand side and move the threshold. The number of sampling points for the function is also too low (see the linear interpolation artefacts).

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


## Sum of Gaussian distributions

Given a distribution of regional brain volumes for a cohort I wanted to display how that distribution can be decomposed into shifted and scaled distributions. A given probablity for regional brain volume and a related distance from the mean is therefore composed of different distances and probabilities in the underlying (covariate of no interest) distributions. Here I wanted to decompose the regional brain volume by age (young and old) and gender (male and female). Each of these distributions is represented with its own graph.

![DVD](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Data.gif)

This actually worked out ok. I was quite happy with this and I discovered the magical function LaggedStart.

```python
class Data(Scene):
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

        gauss_start_graph.add_updater(
            lambda x: x.become(
                axes_start.get_graph(
                    lambda x: alpha_tracker.get_value() * (np.exp(-0.1*(x+3-10)**2)+np.exp(-0.1*(x-3-10)**2)+np.exp(-0.05*(x-0.1-10)**2)+np.exp(-0.05*(x+0.1-10)**2)),
                    color=BLUE
                )
            )
        )
        #self.play(alpha_tracker.animate.set_value(0.5), run_time=2)
        #self.wait()
        self.play(alpha_tracker.animate.set_value(1.0), run_time=3)

        #
        # After we have the summary we can create one more graph for another measure.
        # We need to move the graph down and create a new graph.
        #

        axes1 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, width = FRAME_WIDTH - 0.4)
        axes2 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, width = FRAME_WIDTH - 0.4)
        axes3 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, width = FRAME_WIDTH - 0.4)
        axes4 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, width = FRAME_WIDTH - 0.4)
        axes5 = Axes((-5, 25, 5), (0,3), height= FRAME_HEIGHT/8, width = FRAME_WIDTH - 0.4)

        ax1_labels = axes1.get_x_axis_label("V_{\\text{gender=male}}")
        ax2_labels = axes2.get_x_axis_label("V_{\\text{gender=female}}")
        ax3_labels = axes3.get_x_axis_label("V_{\\text{age=young}}")
        ax4_labels = axes4.get_x_axis_label("V_{\\text{age=old}}")
        ax5_labels = axes5.get_x_axis_label("V")

        all_axes_labels = VGroup(ax1_labels, ax2_labels, ax3_labels, ax4_labels, ax5_labels)
        all_axes_labels.arrange(DOWN, buff=0.4)

        #axes.add_coordinate_labels()
        all_axes = VGroup(axes1, axes2, axes3, axes4, axes5)
        all_axes.arrange(DOWN, buff=0.4)

        gamma_1_tracker = ValueTracker(0.0)
        gamma_2_tracker = ValueTracker(0.0)
        gamma_3_tracker = ValueTracker(0.0)
        gamma_4_tracker = ValueTracker(0.0)

        gauss1_graph = all_axes[0].get_graph(
            lambda x: gamma_1_tracker.get_value() * np.exp(-0.1*(x+3-10)**2), 
            color=GREY
        )

        gauss2_graph = all_axes[1].get_graph(
            lambda x: gamma_2_tracker.get_value() * np.exp(-0.1*(x-3-10)**2), 
            color=GREY
        )

        gauss3_graph = all_axes[2].get_graph(
            lambda x: gamma_3_tracker.get_value() * np.exp(-0.1*(x-0.1-10)**2), 
            color=GREY
        )
        gauss4_graph = all_axes[3].get_graph(
            lambda x: gamma_4_tracker.get_value() * np.exp(-0.1*(x+0.1-10)**2),
            color=GREY
        )
        gauss5_graph = all_axes[4].get_graph(
            lambda x: np.exp(-0.1*(x+3-10)**2)+np.exp(-0.1*(x-3-10)**2)+np.exp(-0.1*(x-0.1-10)**2)+np.exp(-0.1*(x+0.1-10)**2), 
            color=BLUE
        )

        beta_1_tracker = ValueTracker(1.0)
        beta_2_tracker = ValueTracker(1.0)
        beta_3_tracker = ValueTracker(1.0)
        beta_4_tracker = ValueTracker(1.0)

        # a version of the combined graph with parameters
        gauss6_graph = all_axes[4].get_graph(
            lambda x: beta_1_tracker.get_value() * np.exp(-0.1*(x+3-10)**2) + beta_2_tracker.get_value() * np.exp(-0.1*(x-3-10)**2) + beta_3_tracker.get_value() * np.exp(-0.05*(x-0.1-10)**2)+ beta_4_tracker.get_value() * np.exp(-0.05*(x+0.1-10)**2), 
            color=RED
        )

        gauss6_graph.add_updater(
            lambda x: x.become(
                all_axes[4].get_graph(
                    lambda x: beta_1_tracker.get_value() * np.exp(-0.1*(x+3-10)**2) + beta_2_tracker.get_value() * np.exp(-0.1*(x-3-10)**2) + beta_3_tracker.get_value() * np.exp(-0.05*(x-0.1-10)**2)+ beta_4_tracker.get_value() * np.exp(-0.05*(x+0.1-10)**2), 
                    color=RED
                )
            )
        )

        graphs = VGroup(gauss1_graph, gauss2_graph, gauss3_graph, gauss4_graph, gauss5_graph)


        graphs[0].add_updater(
            lambda x: x.become(
                all_axes[0].get_graph(
                    lambda x: gamma_1_tracker.get_value() * np.exp(-0.1*(x+3-10)**2), 
                    color=GREY
                )                
            )
        )
        graphs[1].add_updater(
            lambda x: x.become(
                all_axes[1].get_graph(
                    lambda x: gamma_2_tracker.get_value() * np.exp(-0.1*(x-3-10)**2), 
                    color=GREY
                )
            )
        )
        graphs[2].add_updater(
            lambda x: x.become(
                all_axes[2].get_graph(
                    lambda x: gamma_3_tracker.get_value() * np.exp(-0.05*(x-0.1-10)**2), 
                    color=GREY
                )
            )
        )
        graphs[3].add_updater(
            lambda x: x.become(
                all_axes[3].get_graph(
                    lambda x: gamma_4_tracker.get_value() * np.exp(-0.05*(x+0.1-10)**2), 
                    color=GREY
                )
            )
        )

        #gauss1_label = axes1.get_axis_labels(tex.scale(0.7))
        # gauss1_label = axes1.get_graph_label(gauss1_graph, label='Make')
        #gauss2_label = axes2.get_graph_label(gauss2_graph, label='Female')
        #gauss3_label = axes3.get_graph_label(gauss3_graph, label='Young age')
        gauss5_label = axes5.get_graph_label(gauss5_graph, label='V')

        # put all 4 graphs below each other
        #graphs.arrange(DOWN, buff=1)

        #self.play(Write(axes4, lag_ratio=0.01, run_time=1))
        self.wait(2)
        self.play(
            FadeOut(y_label),
        )
        self.play(
            #Write(graphs[3]),
            #Transform(gauss_start_graph, graphs[3]),
            Transform(axes_start, all_axes[4]),
            Transform(gauss_start_label, gauss5_label),
        )
        self.add(gauss6_graph)
        self.wait(2)

        # Add the copy of our last graph

        ax3_labels = all_axes[3].get_x_axis_label("V_{\\text{age=old}}").scale(0.9).align_to(all_axes[3], RIGHT + UP)
        self.add(ax3_labels)

        self.play(
            Write(all_axes[3], lag_ratio=0.01),
            Write(graphs[3]),
            #Write(all_axes_labels[0]),
            #Transform(graphs[3].copy(), graphs[2]),
            # add gauss2_label
            #Write(gauss2_label),
            #graphs[3].animate.set_color(GREY),
            run_time=1
        )


        self.play(
            beta_4_tracker.animate.set_value(0.0),
            gamma_4_tracker.animate.set_value(1.0),
            run_time=1
        )


        ax2_labels = all_axes[2].get_x_axis_label("V_{\\text{age=young}}").scale(0.9).align_to(all_axes[2], RIGHT + UP)
        self.add(ax2_labels)

        self.play(
            Write(all_axes[2], lag_ratio=0.01),
            Write(graphs[2]),
            #Write(all_axes_labels[0]),
            #Transform(graphs[3].copy(), graphs[2]),
            # add gauss2_label
            #Write(gauss2_label),
            #graphs[3].animate.set_color(GREY),
            run_time=1
        )

        self.play(
            beta_3_tracker.animate.set_value(0.0),
            gamma_3_tracker.animate.set_value(1.0),
            run_time=1
        )

        #self.play(Write(graphs[2]))
        ax1_labels = all_axes[1].get_x_axis_label("V_{\\text{gender=female}}").scale(0.9).align_to(all_axes[1], RIGHT + UP)
        self.add(ax1_labels)

        self.play(
            Write(all_axes[1], lag_ratio=0.01, run_time=1),
            Write(graphs[1]),
            # Write(all_axes_labels[1]),
            #Transform(graphs[3].copy(), graphs[1]),
            #Write(gauss2_label),
        )

        self.play(
            beta_2_tracker.animate.set_value(0.0),
            gamma_2_tracker.animate.set_value(1.0),
        )

        #self.play(Write(graphs[1]))

        self.play(
            Write(all_axes[0], lag_ratio=0.01, run_time=1),
            Write(graphs[0]),
            # Write(all_axes_labels[2]),
            #Transform(graphs[3].copy(), graphs[0]),
        )        
        ax0_labels = all_axes[0].get_x_axis_label("V_{\\text{gender=male}}").scale(0.9).align_to(all_axes[0], RIGHT + UP)
        self.add(ax0_labels)

        self.play(
            beta_1_tracker.animate.set_value(0.0),
            gamma_1_tracker.animate.set_value(1.0),
        )
        self.wait()

        # add all of them again
        self.play(LaggedStart(
                gamma_1_tracker.animate.set_value(0.0),
                gamma_2_tracker.animate.set_value(0.0),
                gamma_3_tracker.animate.set_value(0.0),
                gamma_4_tracker.animate.set_value(0.0),
                lag_ratio=0.25,
            ),LaggedStart(
                beta_4_tracker.animate.set_value(1.0),
                beta_3_tracker.animate.set_value(1.0),
                beta_2_tracker.animate.set_value(1.0),
                beta_1_tracker.animate.set_value(1.0),
                lag_ratio=0.25,
            ),
            run_time=1,
        )
        self.play(LaggedStart(
                gamma_1_tracker.animate.set_value(1.0),
                gamma_2_tracker.animate.set_value(1.0),
                gamma_3_tracker.animate.set_value(1.0),
                gamma_4_tracker.animate.set_value(1.0),
                lag_ratio=0.25,
            ),LaggedStart(
                beta_4_tracker.animate.set_value(0.0),
                beta_3_tracker.animate.set_value(0.0),
                beta_2_tracker.animate.set_value(0.0),
                beta_1_tracker.animate.set_value(0.0),
                lag_ratio=0.25,
            ),
            run_time=1,
        )
        self.remove(gauss6_graph)
```


## Time Variance Authority

Reading a comment to one of our papers I thought that it is not that easy to understand a concept like 'brain state'. The brain is driven by itself and to a smaller degree by external stimuli. If we focus on the internal communication of neurons with each other such interactions have a delay and can form very complex temporal pattern. Every brain piece might be meandering around drunkenly and every once in a while bump against other brain pieces (receive and send). If there are repeating pattern in that kind of network we could classify them as 'brain states'. For example some waves of activity may travel across the brain right when you fall asleep, or if you have a seizure. Other times there might be no waves but more or less synchrony between smaller regions. Maybe some neurons just form a bucket chain of activity that can be arbitrarily long. It is possible that all of these states can be reached without or with minimal  structural change. No region of the brain needs to 'turn off' or even change its mean firing frequency for this to happen. 

Visualizing this concept of a brain state I used 1D Brownian motion. A single dot moves to the right along a time axis. To show how a temporal pattern can evolve I just build-up a histogram. There are some attractors buildin that create higher likelihoods for the 'brain state' to stay in specific regions. Here there are three regions this brain likes to be in, while still happily traversing the whole space of possible states.


![Time Variance Authority](https://github.com/HaukeBartsch/3b1b-vis/blob/main/images/TimeVarianceAuthority.png)


This part was instructive. Its not that difficult to animate something like this if you have a very clear picture in mind of what it should look like. The mp4 movie is just too big as a gif to be played back here. Instead [download and play](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/TimeVarianceAuthority.mp4) the mp4 directly.

Something strange happened when I moved from one laptop to the next with this animation. I had to specify the FRAME_HEIGHT to make it work. Maybe because of a change in the version of manimgl? The aspect ratio was wrong otherwise and the image appeared to be cut off left and right.

```python
class TimeVarianceAuthority(Scene):
    # TODO: add cyclic boundary conditions, switch only one level up or down
    #       This would produce errors at the border with the trails (up down up...)
    coord = (0,0)
    active_band = 0
    band_bars = 17
    bands = 3
    turns = 50
    band_bars_occupancies = np.zeros(bands * band_bars)
    enable_bars = False
    stop_point = False

    def get_rectangle_corners(self, bottom_left, top_right):
        return [
            (top_right[0], top_right[1]),
            (bottom_left[0], top_right[1]),
            (bottom_left[0], bottom_left[1]),
            (top_right[0], bottom_left[1]),
        ]

    def construct(self):
        self.active_band = 1
        self.coord = (0, self.active_band + 0.5) # y values for each x value, start in the middle of the active band
        # probability to move up or down
        probs = [0.05, 0.9, 0.05]
        t_tracker = ValueTracker(0)
        axes_start = Axes((0, 2500, 2500), (0,self.bands), height = FRAME_HEIGHT - 0, width = FRAME_WIDTH - 0.4)
        #self.add(axes_start)

        # drawing object is a line based on values in history
        dot = Dot(axes_start.coords_to_point(self.coord[0], self.coord[1]), color=WHITE, radius=.02)
        tracedPoint = TracingTail(dot.get_center, time_traced=2.5, stroke_width=(0,3), stroke_opacity=[0, 1])
        bars = VGroup()
        bar_height = self.bands/(len(self.band_bars_occupancies))
        for i in range(len(self.band_bars_occupancies)):
            polygon = Polygon(*[
                axes_start.c2p(*i)
                for i in self.get_rectangle_corners( 
                    (0, i*bar_height ),
                    (2500, (i+1)*bar_height - 0.01)
                )
            ], stroke_width=0.04)
            polygon.stroke_width = 0.0
            polygon.set_fill(RED_E, opacity=.5)
            polygon.tmp = i

            polygon.add_updater(
                lambda x: x.set_opacity(1.7 * self.band_bars_occupancies[x.tmp] / (2*max(self.band_bars_occupancies)) if self.enable_bars and sum(self.band_bars_occupancies) > 0 else 0.0)
            )
            bars.add(polygon)

        self.add(bars, dot, tracedPoint)

        def move_coord(x, tracedPoint, probs):
            if self.stop_point:
                return self.coord
            
            if x % 2500 == 0:
                # reset the traced line, by shifting to the left
                tracedPoint.traced_points = [] # [(x[0]-2500, x[1], x[2]) for x in tracedPoint.traced_points]
                self.active_band = np.random.choice([i for i in range(self.bands)])
                #print("active band", self.active_band)
            if x >= self.turns*2500:
                return self.coord
            # fiddle with the probabilities based on active_band
            d = self.coord[1] - (self.active_band + 0.5)
            if d > 0:
                probs = [0.07, 0.9, 0.03]
            else:
                probs = [0.03, 0.9, 0.07]
            self.coord = (x, self.coord[1] + np.random.choice([-5, 0, 5], p=probs)/100.0)
            #self.coord = (x, 0.5)
            # update the occupancy of each band_bar
            if self.enable_bars:
                y = math.floor(  max(0, min(1.0, (self.coord[1] / self.bands))) * (self.bands * self.band_bars) )
                self.band_bars_occupancies[y] += 1
            #print(self.coord, self.active_band, self.band_bars_occupancies)
            return self.coord

        dot.add_updater(
            lambda x: x.become(
                Dot(axes_start.coords_to_point(self.coord[0] % 2500, move_coord(t_tracker.get_value(), tracedPoint, probs)[1]), radius=.03, color=WHITE)
            )
        )
        self.stop_point = False
        t1 = Text(r"A brain state", font_size=24)
        self.play(Write(t1))
        self.wait()
        t2 = Text(r"is not stationary", font_size=24)
        self.play(FadeOut(t1))
        self.play(FadeIn(t2))
        self.wait()
        self.play(FadeOut(t2))
        # You can be awake, or sleeping.
        # Or focused on work, or enjoying the sun.
        # But what happens if you get stuck,
        # too focused on negative thought, or too self-conscious?
        #  


        self.play(
            t_tracker.animate.set_value(2*2500),
            run_time=2*10,
            rate_func=linear
        )
        self.stop_point = True
        self.wait()
        self.enable_bars = True
        self.stop_point = False
        self.play(
            t_tracker.animate.set_value(self.turns*2500),
            run_time=self.turns*10,
            rate_func=linear
        )
        self.wait()
```

## Bootstrapping A.I. learning

The take-away from this animation was that it is better to work with smaller pieces instead of trying to do everything in one long script.

Given a region of interest (mask) for an image we can compute many values. Whereas the pixel values in the image do not have a meaning assigned to them the values we compute do. For example a 'size of the tumor' - value. So how to we get an A.I. to create those masks for us?

![Bootstrapping A.I. learning](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Anim01.gif)

I am using comments to document what the sub-titles could be (generated by something like Elevenlabs). Interesting pieces here are the grid creation to duplicate objects and iterating over them. Transforms seem to change the origin, after a transform keep working with those objects (not the targets). Alignment is heavily used here as well. 

```python
class Anim01(Scene):
    def construct(self):

        #
        # Text for this teach
        # -------------------
        # How to accellerate AI by iterated integration
        #
        # A medical image and a mask that outlines regions of interest. 
        # 
        # What can we do with such a mask? Calculate biomarkers for example for size, shape, image intensity and texture properties.
        # 
        # While useful for research such masks need to be specificly derived from each image. So how do we get them?
        #
        # How how do we get them for many many images? Lets see how artificial intelligence and more specifically convolutional neural networks can help us accomplish this, without requiring extensive manual work.
        #
        # Convolutional networks are trained using examples. We can generate them by randomly picking a minimum set of examples. Lets say these 10 from the 100 we need to process in our hypothetical project.
        #
        # We manually segment all 10.
        #
        # And train our first artifical intelligence. 
        #
        # That A. I. can probably generate some more of the required masks.
        #
        # Whereas others will be bad or missing. Reviewing all masks is a much easier than manual segmentation.
        #
        # One strategy is to pick those bad samples and do some more manual segmentation on those.
        # 
        # Now we have twice as many good examples. Training now a better A. I..
        # 
        # Maybe we are done now and version 2 will work for everything else we use it for.
        # 
        # Maybe we need to repeat the process. In the meantime many more images will be successfully processed using our A. I. iterations.
        #
        # As all masks are reviewed by a human we can collect examples for failed masks over time.
        #

        squareI = Square(color=WHITE, fill_color=BLACK, fill_opacity=1, stroke_width=0.1)
        self.play(Write(squareI))
        self.wait()
        # add a text to the center of the box
        I_text = Text("Image")
        I_text.move_to(squareI.get_center())
        self.play(Write(I_text))

        self.play(
            squareI.animate.shift(1.2 * LEFT),
            I_text.animate.shift(1.2 * LEFT)
        )

        squareM = Square(color=WHITE, fill_color=GREY, fill_opacity=0.2, stroke_width=0.1)
        # add a text to the center of the box
        M_text = Text("Mask")
        M_text2 = Text("?")
        M_text.move_to(squareM.get_center())
        M_text2.move_to(squareM.get_center())
        #self.play(Write(I_text), Write(M_text))

        # Add what is the goal -> get an AI to compute the mask for us
        # Add different ways to select a subset of the images for segmentation (10%, 50%, 100%)?
        # Limiting resource is human time to segment the images

        squareM.shift(1.2 * RIGHT)
        M_text.shift(1.2 * RIGHT)
        M_text2.shift(1.2 * RIGHT)
        self.play(Write(squareM), Write(M_text))
        self.wait(2)

        # what can we do with the mask?
        meas01 = Text("Size")
        meas02 = Text("Shape")
        meas03 = Text("Intensity")
        mean04 = Text("Texture")
        measures = VGroup(meas01, meas02, meas03, mean04)
        measures.arrange(DOWN, buff=0.5)
        measures.align_on_border(LEFT)
        measures.next_to(squareM, RIGHT)
        measures.shift(0.5 * RIGHT)
        [self.play(Write(x)) for x in measures]
        self.wait(2)
        self.play(FadeOut(measures))
        self.wait(2)

        self.play(Transform(M_text, M_text2))
        self.wait(2)


        one = VGroup(squareI, squareM)

        self.play(FadeOut(M_text), FadeOut(I_text))

        # duplicate the group 10 x 10 times
        all = VGroup(*[one.copy().scale(0.2) for x in range(100)])
        all2 = VGroup(*[one.copy().scale(0.1) for x in range(100)])
        all2.arrange_in_grid(10, 10, buff=0.1)
        all2.move_to([-4, 2, 0])

        self.play(
            FadeOut(one),
            all.animate.arrange_in_grid(10, 10, buff=0.25)
        )
        self.wait()

        # show question marks inside each label box
        qmarks = VGroup()
        for i in range(100):
            q = M_text2.copy()
            q.move_to(all[i][1].get_center())
            qmarks.add(q)
            #self.play(
            #    Write(q),
            #    run_time=0.001
            #)
            #self.wait(0.001)
        self.play(FadeIn(qmarks))
        self.wait()
        self.play(FadeOut(qmarks))

        self.play(
            Transform(all, all2)
        )
        self.wait(2)

        # select 10 random groups
        rs = np.arange(100)
        np.random.shuffle(rs)
        r = rs[:10]
        selected = [all2[i] for i in r]

        self.play(
            LaggedStart(*[selected[i].animate.set_color(BLUE) for i in range(10)], lag_ratio=0.3)
        )
        self.wait()

        # next take the 10 tagged and move them to a column on the right
        self.play(
            *[selected[i].animate.shift(4 * RIGHT) for i in range(10)]
        )
        column = VGroup(*selected)
        column2 = column.copy()
        column2.arrange_in_grid(10, 1, buff=0.1).align_to(all2, TOP)
        self.play(
            Transform(column, column2)
        )

        # now perform manual segmentation, in order, top to bottom
        for i in range(10):
            self.play(
                column[i][1].animate.set_color(GREEN).set_opacity(1.0),
                all[r[i]][1].animate.set_color(GREEN).set_opacity(1.0),
            )
            self.wait(0.5)

        # now train an AI core version 0
        model0 = Square(color=WHITE, fill_color=BLUE, fill_opacity=1.0, stroke_width=0.1)
        model0_text = Tex("\\mathtt{AI}")
        model0_text.move_to(model0.get_center())
        Model0Box = VGroup(model0, model0_text)
        Model0Box.scale(0.5)
        Model0Box.next_to(column, RIGHT)
        self.play(Write(Model0Box), run_time=2)
        self.wait(2)

        # move the column and the AI box closer to the left
        self.play(
            column.animate.shift(0.5 * LEFT),
            Model0Box.animate.shift(0.5 * LEFT)
        )

        # use the AI to segment each image
        boxesRight = VGroup()
        for i in range(100):
            obj = all[i].copy()
            obj[0].shift(8 * RIGHT)
            obj[1].shift(8 * RIGHT)
            opacity = 0.5
            col = BLUE
            if i in r:
                opacity = 1.0
                col = GREEN_E
            #obj[0].set_stroke(width=0.1, color=WHITE)
            self.play(
                obj[1].animate.set_color(col).set_opacity(opacity).set_stroke(width=0.1, color=WHITE),
                obj[0].animate.set_color(BLACK).set_stroke(width=0.1, color=WHITE),
                run_time=0.01
            )
            boxesRight.add(obj)
            self.wait(0.001)

        # now verify manually the blue result boxes (make them green as well)
        r2 = rs[10:20]
        #selected2 = [boxesRight[i] for i in r2]
        for i in range(100):
            if i in r:
                # nothing to do, already green
                continue
            self.play(
                boxesRight[i][1].animate.set_color(GREEN_A).set_opacity(1.0),
                run_time=0.001
            )
            self.wait(0.001)

        self.wait()
        # highlight some broken images
        self.play(
            *[boxesRight[i][1].animate.set_color(RED).set_opacity(1.0) for i in r2]
        )
        self.wait()

        # now extract the broken images and fix them


        broken = VGroup()
        for i in r2:
            bb = VGroup(boxesRight[i][0].copy(), boxesRight[i][1].copy())
            broken.add(bb)

        # duplicate the already done images
        column2 = column.copy()
        column2.move_to(0.5 * BOTTOM + 1.2 * LEFT)
        #self.play(Write(column2))
        self.play(Transform(column, column2))
        self.wait()

        # move the broken images to the right
        self.play(
            *[broken[i].animate.shift(4.5 * LEFT + 1.0 * BOTTOM) for i in range(10)],
        )
        column3 = VGroup(*broken)
        column4 = column3.copy()
        column4.arrange_in_grid(10, 1, buff=0.1).align_to(column, TOP).shift(0.5 * LEFT)
        for obj in column4:
            obj[1].set_color(RED)
            obj[0].set_color(BLUE)
        self.play(
            Transform(column3, column4),
        )
        self.wait()

        # animate the second segmentation step
        for i in range(10):
            self.play(
                column3[i][1].animate.set_color(GREEN).set_opacity(1.0),
                all[r2[i]][1].animate.set_color(GREEN).set_opacity(1.0),
                boxesRight[r2[i]][1].animate.set_color(GREEN).set_opacity(1.0),
            )
            self.wait(0.5)
        
        # now move column3 a little to the left and train another AI (version 2)
        model1 = Square(color=WHITE, fill_color=BLUE, fill_opacity=1.0, stroke_width=0.1)
        model1_text = Tex("\\mathtt{AI}^2")
        model1_text.move_to(model1.get_center())
        model0_text2 = Tex("\\mathtt{AI}^1")
        model0_text2.move_to(model0.get_center()).scale(0.5)
        Model1Box = VGroup(model1, model1_text)
        Model1Box.scale(0.5)
        Model1Box.next_to(column4, RIGHT)
        self.play(Write(Model1Box), Transform(model0_text, model0_text2),
            run_time=2)
        self.wait(2)

        # make our first model the model 0
        self.play(Transform(model0_text, model0_text2))

        # continue with model 3 if needed
        arrow = Arrow(start=LEFT, end=RIGHT)
        arrow.next_to(Model1Box, RIGHT)
        self.play(Write(arrow))
        self.wait()

        model2 = Square(color=WHITE, fill_color=BLUE, fill_opacity=1.0, stroke_width=0.1)
        model2_text = Tex("\\mathtt{AI}^3")
        model2_text.move_to(model2.get_center())
        Model2Box = VGroup(model2, model2_text)
        Model2Box.scale(0.5)
        Model2Box.next_to(arrow, RIGHT)
        self.play(Write(Model2Box), run_time=2)
        self.wait(2)

```

## DICOM image meta information

I wanted to show that medical images contain metadata inside and how we can transform them into research data by adding three pieces of information, the project name, the pseudonymized participant ID and the visit / event.

![Clinical to research data transformation](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Anim02.gif)

Very straight forward. The tricky bit was to keep the alignment of the individual text elements. I had to add characters that fill the full font-height and make them invisible to make it work. I also found a solution to the z-stacking issue from my first attempt. Turns out that setting z_index instead of calling set_z did the trick.

```python
class Anim02(Scene):
    def construct(self):
        rect_c = RoundedRectangle(corner_radius=0.5, height=4.0, width=4.0, fill_color=BLUE, fill_opacity=1)
        rect_c.z_index = 2
        self.play(Write(rect_c))
        t_image = Text("image")
        t_image.next_to(rect_c, UP)
        self.play(Write(t_image))
        self.wait()
        self.play(rect_c.animate.shift(3 * LEFT), t_image.animate.shift(3 * LEFT))

        # mention image + WHO WHERE WHAT HOW
        t_meta = Text("what + who + when + how + where")
        t_meta.next_to(rect_c, UP).shift(6*RIGHT)
        self.play(Write(t_meta))
        self.wait()

        t = Text("Modality: MR")
        t2 = Text("Patient name: Hauke Bartschj")
        t2[24].set_opacity(0)
        t3 = Text("Date of birth: 1970-01-01j")
        t3[22].set_opacity(0)
        t4 = Text("Study date: 2021-01-01")
        t5 = Text("Study description: chest abdomen")
        t6 = Text("Protocol name: T2W_TSE SENSE")

        # Add info about imaging physics, protocol, space and time (WHERE WHAT AND HOW)
        # 100 times more meta-data info than images in a DICOM file

        g = VGroup(t, t2, t3, t4, t5, t6)
        g.z_index = 3
        g.arrange(DOWN, buff=0.1, center=False, aligned_edge=LEFT)
        g.next_to(rect_c, RIGHT)
        self.play(Write(g),FadeOut(t_image), FadeOut(t_meta))
        self.wait()

        # show ok data, show sensitive data
        self.play(t.animate.set_color(GREEN),
                  t5.animate.set_color(GREEN),
                  t6.animate.set_color(GREEN))
        self.wait()
        self.play(t2.animate.set_color(RED),
                  t3.animate.set_color(RED))
        #self.wait()
        #self.play(t4.animate.set_color(YELLOW))
        self.wait(2)

        self.play(
            t.animate.set_color(WHITE),
            t2.animate.set_color(WHITE),
            t3.animate.set_color(WHITE),
            t4.animate.set_color(WHITE),
            t5.animate.set_color(WHITE),
            t6.animate.set_color(WHITE)
        )

        # show that they are part of the image (meta-data)
        g.scale(0.5)
        g2 = g.copy()
        [x.set_color(BLACK) for x in g2]
        g2.move_to(rect_c.get_center())
        self.play(Transform(g, g2))
        self.wait(2)

        copy_of_g2 = g2.copy()
        #copy_of_g2.set_color(GREY_B)

        c_txt = Text("Clinic")
        c_txt.next_to(rect_c, DOWN) 
        self.play(Write(c_txt))

        self.wait()

        #
        # Show what we can do with an image + meta data
        # (send around)
        ar = Arrow(start=LEFT, end=RIGHT)
        ar.next_to(rect_c, RIGHT)
        ar_txt = Text("send")
        ar_txt.next_to(ar, UP)
        self.play(GrowArrow(ar), Write(ar_txt))

        destination1 = Text("Stavanger",font_size=65)
        destination1.next_to(ar, RIGHT)
        destination2 = Text("Førde",font_size=65)
        destination2.next_to(ar, RIGHT)
        destination3 = Text("Fonna",font_size=65)
        destination3.next_to(ar, RIGHT)
        destination4 = Text("Haugesund",font_size=65)
        destination4.next_to(ar, RIGHT)
        destination5 = Text("Ålesund",font_size=65)
        destination5.next_to(ar, RIGHT)
        self.wait()
        destination6 = Text("Australia",font_size=65)
        destination6.next_to(ar, RIGHT)
        self.play(Write(destination1))
        self.play(Transform(destination1, destination2))
        self.play(Transform(destination1, destination3))
        self.play(Transform(destination1, destination4))
        self.play(Transform(destination1, destination5))
        self.play(Transform(destination1, destination6))

        self.wait(2)
        self.play(FadeOut(ar), FadeOut(ar_txt), FadeOut(destination1))



        rect_r = RoundedRectangle(corner_radius=0.5, height=4.0, width=4.0, fill_color=GREEN, fill_opacity=1)
        rect_r.shift(3 * LEFT)
        rect_r.z_index = 0

        r_txt = Text("Research")
        r_txt.next_to(rect_r, DOWN).shift(6 * RIGHT)
        #self.play(Write(c_txt))
        self.play(FadeIn(r_txt))

        qm = Text("?", font_size=44)
        qm.move_to(rect_r.get_center())
        qm.z_index = 1
        self.play(Write(qm))

        # fix to get research ready data
        self.play(rect_r.animate.shift(6*RIGHT),
                  qm.animate.shift(6*RIGHT))
        self.wait()
        self.play(FadeOut(qm))

        # now move over the research identity
        t_project = Text("Project: GEMRIC", font_size=24)
        t_event = Text("Event: week 052j", font_size=24)
        t_event[13].set_opacity(0)
        t_subject = Text("Participant: GEMRIC_01_001", font_size=24)
        r_ident = VGroup(t_project, t_event, t_subject)
        r_ident.arrange(DOWN, buff=0.1, center=False, aligned_edge=LEFT)
        r_ident.next_to(rect_r, UP)
        self.play(Write(r_ident))

        self.wait()

        # animate the different texts for event and participant
        t_event2 = Text("Event: baselinej", font_size=24).move_to(t_event, LEFT)
        t_event2[14].set_opacity(0)
        t_event3 = Text("Event: day 1j", font_size=24).move_to(t_event, LEFT)
        t_event3[10].set_opacity(0)
        t_event4 = Text("Event: week 1j", font_size=24).move_to(t_event, LEFT)
        t_event4[11].set_opacity(0)
        t_event5 = Text("Event: week 26j", font_size=24).move_to(t_event, LEFT)
        t_event5[12].set_opacity(0)
        self.play(
            FadeOut(t_event), 
            FadeIn(t_event2)
        )
        self.play(            
            FadeOut(t_event2),
            FadeIn(t_event3)
        )
        self.play(            
            FadeOut(t_event3), 
            FadeIn(t_event4),
        )
        self.play(            
            FadeOut(t_event4), 
            FadeIn(t_event5),
        )
        self.wait()

        t_part2 = Text("Participant: GEMRIC_01_001", font_size=24).move_to(t_subject, LEFT)
        t_part3 = Text("Participant: GEMRIC_01_002", font_size=24).move_to(t_subject, LEFT)
        t_part4 = Text("Participant: GEMRIC_02_001", font_size=24).move_to(t_subject, LEFT)
        t_part5 = Text("Participant: GEMRIC_01_999", font_size=24).move_to(t_subject, LEFT)
        self.play(
            FadeOut(t_subject), 
            FadeIn(t_part2)
        )
        self.play(            
            FadeOut(t_part2),
            FadeIn(t_part3)
        )
        self.play(            
            FadeOut(t_part3), 
            FadeIn(t_part4),
        )
        self.play(            
            FadeOut(t_part4), 
            FadeIn(t_part5),
        )
        self.wait()
        # now create the resulting info text for research purposes

        t_r = Text("Modality: MR")
        t2_r = Text("Patient name: GEMRIC_01_999j")
        t2_r[25].set_opacity(0)
        t3_r = Text("Date of birth:j")
        t3_r[12].set_opacity(0)
        t4_r = Text("Study date: 2021-02-15 (+X days)")
        t5_r = Text("Study description: Check for brain")
        t6_r = Text("Event: week 26j")
        t6_r[12].set_opacity(0)
        t7_r = Text("Project: GEMRIC")
        t8_r = Text("Protocol name: T2W_TSE SENSE")
        g2_r = VGroup(t_r, t2_r, t3_r, t4_r, t5_r, t6_r, t7_r, t8_r)
        g2_r.arrange(DOWN, buff=0.1, center=False, aligned_edge=LEFT)
        g2_r.move_to(rect_r.get_center())
        g2_r.scale(0.5)
        #self.play(Write(g2_r))
        self.play(Transform(t, t_r))
        self.play(Transform(t_part5, t2_r))
        #self.play(FadeOut(t2))
        #self.play(FadeOut(t3), FadeIn(t3_r))
        self.play(FadeIn(t3_r))
        self.play(Transform(t4, t4_r))
        self.play(Transform(t5, t5_r))
        self.play(Transform(t_event5, t6_r))
        #self.play(Transform(t_part5, t5_r))
        self.play(Transform(t_project, t7_r))
        self.play(Transform(t6, t8_r))
        # now hide the outside values
        #self.play(FadeOut(t_part5))
        #self.play(FadeOut(t_event5))
        self.play(FadeOut(t2), FadeOut(t3), FadeIn(copy_of_g2))
        self.wait()
```

## The role of FIONA

The FIONA box performs the above transformation from clinical data into research data. All data is structured nicely inside the research PACS (picture archive and communication system).

![data transformation with FIONA](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Anim03.gif)

Same tricks as in the above section. I had to figure out how to left align the text for each box. I ended up with a somewhat ok fit. It would be nicer to have a better layout engine.

```python
class Anim03(Scene):
    def construct(self):
        rect_c = RoundedRectangle(corner_radius=0.5, height=3.0, width=3.0, fill_color=BLUE, fill_opacity=1)
        rect_c.z_index = 1
        self.play(Write(rect_c))
        self.wait()
        self.play(rect_c.animate.shift(4.5 * LEFT))

        clinic = Text("clinic")
        clinic.z_index = 1
        clinic.move_to(rect_c, TOP).shift(2.0 * UP)
        self.play(FadeIn(clinic))

        # where we want to go
        pacs = Text("research PACS")
        pacs.z_index = 1
        pacs.move_to(rect_c, TOP).shift(2.0 * UP + 9.5 * RIGHT)
        self.play(FadeIn(pacs))


        square = Rectangle(fill_color=GREY, height=5.0, width=4.5)
        #square.shift(1 * RIGHT)
        square.z_index = 0
        fiona = Text("FIONA")
        fiona.align_to(square, TOP).shift(0.2 * DOWN + 1 * LEFT)
        g = VGroup(square, fiona)
        self.play(Write(g))

        p = Text("Project")
        n = Text("Namej")
        n[4].set_opacity(0)
        e = Text("Eventj")
        e[5].set_opacity(0)
        g1 = VGroup(p, n, e)
        g1.arrange(DOWN, buff=0.1, center=False, aligned_edge=LEFT)
        g1.shift(1.2 * LEFT + 1.0 * UP)
        
        pb = Rectangle(height=0.46, width=2, fill_color=GREY,color=WHITE)
        nb = Rectangle(height=0.46, width=2, fill_color=GREY,color=WHITE)
        eb = Rectangle(height=0.46, width=2, fill_color=GREY,color=WHITE)
        g2 = VGroup(pb, nb, eb)
        g2.arrange(DOWN, buff=0.1, center=False, aligned_edge=LEFT)
        g2.move_to(g1.get_right(),LEFT).shift(0.3 * RIGHT)
        self.play(Write(g1), Write(g2))

        # move the data to fiona, change color, send to research PACS
        rect_r = rect_c.copy()
        rect_r.shift(4.5 * RIGHT + 1.5 * DOWN)
        rect_r.scale(0.5)
        self.play(Transform(rect_c, rect_r))

        self.wait()
        self.play(rect_r.animate.set_color(GREEN), run_time=0.1)

        # send to PACS now
        rect_p = rect_r.copy()
        rect_p.shift(4* RIGHT + 3.5 * UP)
        rect_p.scale(0.5)
        self.play(Transform(rect_r, rect_p))
        self.play(FadeOut(rect_c))
        self.wait()

        # do it again, but faster
        rect_c = RoundedRectangle(corner_radius=0.5, height=3.0, width=3.0, fill_color=BLUE, fill_opacity=1)
        rect_c.z_index = 1
        rect_c.shift(4 * LEFT)
        self.play(FadeIn(rect_c))

        rect_r = rect_c.copy()
        rect_r.shift(4 * RIGHT + 1.5 * DOWN)
        rect_r.scale(0.5)
        self.play(Transform(rect_c, rect_r))

        self.wait()
        self.play(rect_r.animate.set_color(GREEN), run_time=0.1)

        # send to PACS now
        rect_p = rect_r.copy()
        rect_p.shift(5.0 * RIGHT + 3.5 * UP)
        rect_p.scale(0.5)
        self.play(Transform(rect_r, rect_p))
        self.play(FadeOut(rect_c))
        #self.wait()

        # just show what happens over time by adding more fields
        # do it again, but faster
        rect_c = RoundedRectangle(corner_radius=0.5, height=3.0, width=3.0, fill_color=BLUE, fill_opacity=1)
        rect_c.z_index = 1
        rect_c.shift(4 * LEFT)
        self.play(FadeIn(rect_c))

        rect_r = rect_c.copy()
        rect_r.shift(4 * RIGHT + 1.5 * DOWN)
        rect_r.scale(0.5)
        self.play(Transform(rect_c, rect_r))

        self.wait()
        self.play(rect_r.animate.set_color(GREEN), run_time=0.1)

        # send to PACS now
        rect_p = rect_r.copy()
        rect_p.shift(6.0 * RIGHT + 3.5 * UP)
        rect_p.scale(0.5)
        self.play(Transform(rect_r, rect_p))
        self.play(FadeOut(rect_c))
        self.wait()

        # show that the individual projects appear together in research PACS
        squareP1 = Rectangle(fill_color=GREY, height=1.5, width=3.0)
        squareP1.shift(5*RIGHT + 2.0 * UP)
        #square.shift(1 * RIGHT)
        squareP1.z_index = 0
        #pacs = Text("research PACS")
        #pacs.z_index = 1
        #pacs.move_to(squareP1, TOP).shift(0.8 * UP)
        #g = VGroup(squareP1, pacs)
        self.play(Write(squareP1))

        # lets make the green squares disappear?        

        squareP2 = Rectangle(fill_color=GREY, height=1.5, width=3.0)
        squareP2.shift(5*RIGHT + 0 * UP)
        #square.shift(1 * RIGHT)
        squareP2.z_index = 0

        squareP3 = Rectangle(fill_color=GREY, height=1.5, width=3.0)
        squareP3.shift(5*RIGHT - 2 * UP)
        #square.shift(1 * RIGHT)
        squareP3.z_index = 0
        self.play(Write(squareP2), Write(squareP3))
```

## Counting pixel

This one was fun. I wanted to do a 'what if this is a pile of rice' analogy. I ended up just counting all pixel values in one research project.

![How many values?](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/BigData.gif)

Working with time was more complex than it needed to be. I think some better easing functions are needed.

```python
class BigData(Scene):
    numbers = VGroup()
    texts = VGroup()
    nums = [ValueTracker(0), ValueTracker(0), ValueTracker(0), ValueTracker(0), ValueTracker(0), ValueTracker(0) ]
    square_height = ValueTracker(0.001)

    def construct(self):

        bsquare = Rectangle(width=2, height=2)
        bsquare.set_z(1)
        bsquare.set_fill(BLACK, 1)
        bsquare.shift(LEFT * 2 + DOWN)
        self.add(bsquare)

        square = Rectangle(width=2, height=self.square_height.get_value())
        square.add_updater(lambda m: m.set_height(2*self.square_height.get_value(),stretch=True, about_edge=DOWN))
        square.set_z(0)
        square.set_fill(BLUE, 1)
        #square.shift(LEFT * 2 + DOWN)
        square.move_to(bsquare).shift(DOWN)
        self.play(FadeIn(square))

        txts = ["pixels", "images", "series", "visits", "participants", "project" ]
        tick_over = [ 1, 2200 * 2400, 2200 * 2400 * 380, 2200 * 2400 * 380 * 12, 2200 * 2400 * 380 * 12 * 4, 2200 * 2400 * 380 * 12 * 4 * 30000]

        def num2parts(n, tick_over):
            res = [ n // tick_over[0] ]
            for i in range(1, len(tick_over)):
                res.append( n // tick_over[i] )
            return res

        def humanize_number(value, fraction_point=1):
            l1 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100]
            l1.reverse()
            powers = [10 ** x for x in tuple(l1)]
            human_powers = [ ' thousand', ' million', ' billion', ' trillion', ' quadrillion',
                ' quintillion', ' sextillion', ' septillion',
                ' octillion', ' nonillion', ' decillion', ' googol' ]
            human_powers.reverse()
            human_powers = tuple(human_powers)

            #powers = [10 ** x for x in self.powers.reverse()]
            # human_powers = self.human_powers.reverse()
            return_value = ""
            is_negative = False
            if not isinstance(value, float):
                value = float(value)
            if value < 0:
                is_negative = True
                value = abs(value)
            for i, p in enumerate(powers):
                if value >= p:
                    return_value = str(round(value / (p / (10.0 ** fraction_point))) /
                                    (10 ** fraction_point)) + human_powers[i]
                    break
            if is_negative:
                return_value = "-" + return_value

            return return_value

        n_ar = []
        for i in range(0,len(self.nums)):
            #print(i)
            t = Text(str(int(self.nums[i].get_value())), font_size=64)
            t.tmp = i
            #t.shift(RIGHT * 4 + UP * (2-i))
            t.add_updater(
                lambda m:
                    m.become(Text("{:,.0f}".format(self.nums[m.tmp].get_value()), font_size=64).to_edge(UR).shift( LEFT * 2 + DOWN * (m.tmp) + DOWN)))
            self.numbers.add(t)

            t2 = Text(txts[i], font_size=32)
            t2.always.next_to(t, RIGHT)
            self.texts.add(t2)
        self.add(self.numbers, self.texts)
        self.wait(2)

        # now animate the counter ticking up
        speeds = [1, 1000, 1000000, 1000000000, 10000000000000]
        when = [speeds[0]*40, speeds[1]*100, speeds[2]*100, speeds[3]*100, speeds[4]*100]
        counter = 0
        stop = False
        t = 0
        while (not(stop)):
            if counter > tick_over[-1]:
                stop = True
            if counter > when[t]:
                if t < len(speeds)-1:
                    t += 1
                    self.wait(0.5)
            ns = num2parts(counter, tick_over)
            #print(ns)
            #print(humanize_number(ns[0]))
            #self.nums[0].set_value(ns[0])
            for j in range(0,len(self.nums)):
                self.nums[j].set_value(ns[j])
            counter += speeds[t]

            self.square_height.set_value(0.01 + 0.99 * (counter / tick_over[-1]))
            #print(square_height.get_value())
            self.wait(0.05)
        self.wait()

        tt = Text( humanize_number(ns[0]) + " values", font_size=64 )
        tt.shift(2.75 * DOWN + 2 * LEFT)
        self.play(FadeIn(tt))
        self.wait(3)
```

## Access for Safe

Safe is the shared compute environment of the University of Bergen, Norway. Its suitable for sensitive data and provides REDCap access as well as scalable Windows and Linux compute resources. Because its a heterogenous system and secure data access and data transfers are limited. To explain what that entails I create the following data flow graph animation.

![How data goes into Safe](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/AccessSafe.gif)

The only new thing here is the use of an external svg file during the animation.

```python
class AccessSafe(Scene):
    def construct(self):

        square = Rectangle(width=4,height=1.8)
        square.set_fill(BLUE, 1)
        safe_txt = Text("Safe")
        safe_txt.move_to(square.get_center())
        box = VGroup(square, safe_txt)
        self.play(Write(box))
        self.wait()


        self.play(box.animate.shift(2* UP),square.animate.set_opacity(0))

        squareW = Square(color=WHITE, fill_color=BLUE, fill_opacity=1.0, stroke_width=1)
        squareW.move_to(1.5*LEFT)
        w_txt = Text("Windows", font_size=28)
        w_txtR = Text("Henderson", font_size=28)
        w_txt.move_to(squareW.get_center())
        w_txtR.move_to(squareW.get_center())
        box2 = VGroup(squareW, w_txt)

        self.play(Write(box2))

        squareL = Square(color=WHITE, fill_color=BLUE, fill_opacity=1.0, stroke_width=1)
        squareL.move_to(2.0*RIGHT)
        l_txt = Text("Linux", font_size=28)
        l_txt.move_to(squareL.get_center())
        l_txtR = Text("Homlungen", font_size=28)
        l_txtR.move_to(squareL.get_center())
        box3 = VGroup(squareL, l_txt)

        self.play(Write(box3))


        # add the arrows
        arrow_1 = Arrow(start=LEFT, end=RIGHT, color=GOLD)
        arrow_1.next_to(box2, LEFT)
        rdp_text = Text("RDP")
        rdp_text.next_to(arrow_1, DOWN)
        self.play(Write(arrow_1))
        self.wait()
        self.play(Write(rdp_text))
        self.wait()
        #self.play(FadeOut(rdp_text))



        arrow_2 = Arrow(start=squareW.get_right(), end=squareL.get_left(), color=GOLD)
        arrow_2.next_to(box2, RIGHT)
        self.play(Write(arrow_2))
        self.wait()
        rdp_text2 = Text("RDP")
        rdp_text2.next_to(arrow_2, DOWN)
        self.play(Write(rdp_text2))
        self.wait()
        #self.play(FadeOut(rdp_text2))


        self.wait()
        self.play(Transform(w_txt, w_txtR))
        self.wait()
        self.play(Transform(l_txt, l_txtR))
        self.wait(2)

        # issue with uploading files
        file = SVGMobject("assets/file-arrow-up-alt-svgrepo-com.svg")
        file.scale(0.4)
        file.set_stroke(WHITE, 6)
        file.next_to(arrow_1, UP)
        self.play(Write(file))


        self.play(file.animate.shift(0.5*RIGHT))
        file.set_stroke(RED, 6)
        self.play(file.animate.shift(0.5*LEFT))
        self.play(file.animate.shift(0.5*RIGHT))
        self.play(file.animate.shift(0.5*LEFT))
        self.wait(2)
        self.play(FadeOut(rdp_text), FadeOut(rdp_text2))


        # upload data to display.uib.no
        display_t = Text("desktop.uib.no", font_size=28)
        display = Square(color=WHITE, fill_color=BLUE, fill_opacity=0.1, stroke_width=0.1)
        display.move_to(1.5*LEFT + 2.5 * DOWN)
        display_t.move_to(display.get_center())
        box3 = VGroup(display, display_t)
        self.play(Write(box3))

        arrow_3 = Arrow(start=LEFT, end=RIGHT, color=GOLD)
        arrow_3.next_to(box3, LEFT)
        rdp_text3 = Text("RDP")
        rdp_text3.next_to(arrow_3, DOWN)
        self.play(Write(arrow_3))
        self.play(Write(rdp_text3))
        self.wait()


        file2 = SVGMobject("assets/file-arrow-up-alt-svgrepo-com.svg")
        file2.scale(0.4)
        file2.set_stroke(WHITE, 4)
        file2.next_to(arrow_3, UP)
        self.play(Transform(file, file2))
        self.wait(2)
        self.play(file.animate.scale(0.5).set_stroke(GREEN, 2).next_to(display_t.get_center(), UP))

        file3 = file2.copy()
        file3.scale(0.5)
        file3.next_to(w_txtR, DOWN)

        file4 = file2.copy()
        file4.scale(0.5)
        file4.next_to(l_txtR, DOWN)
        self.play(FadeOut(file))
        self.wait()
        self.play(FadeIn(file3),FadeIn(file4))
        self.wait(2)

        # hide display again
        self.play(FadeOut(box3),FadeOut(arrow_3),FadeOut(rdp_text3))
```

## Physics simulation

In order to show how far I got with learning the ropes here a Lattice Boltzmann (2D9Q) animation with reflective and periodic boundary conditions (no-slip). The original python code is from the Wikipedia page and adapted here to 3b1b. The lattice on the left is using reflective, the lattice on the right periodic boundary conditions.

![Lattice Boltzman animation](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/LB.gif)

Each of the two fields has a resolution of 50 by 50. The _LB class performs the computation and vis() the drawing at each timestep. The two lattices are displayed using a grid of circles. Outside an annulus ring the opacity of the circles is set to very low. This was the first time I tried to use colormaps - in this case just a transition map between two colors.

```python
from manimlib import *
import math

def sum(a):
    s=0
    for e in a:
        s=s+e
    return s

class Field2D():
    def __init__(self,res : int):
        self.field=[]
        for b in range(res):
            fm=[]
            for a in range(res):
                fm.append([0,0,0,
                           0,1,0,
                           0,0,0])
            self.field.append(fm[:])
        self.res = res
    # Momentum of the field
    def Momentum(self,x,y,velocityField):
        return velocityField[y][x][0]*sum(self.field[y][x]),velocityField[y][x][1]*sum(self.field[y][x])

class _LB():
    res = 50
    _field = None
    Weights = [ 1/36, 1/9, 1/36, 1/9, 4/9, 1/9, 1/36, 1/9, 1/36 ]
    DiscreteVelocityVectors = [ [-1,1], [0,1], [1,1], [-1,0], [0,0], [1,0], [-1,-1], [0,-1], [1,-1] ]
    velocityField = []
    DensityField = []
    SpeedOfSound = 1/math.sqrt(3)
    # The speed of sound, specifically 1/sqrt(3) ~ 0.57
    TimeRelaxationConstant = 0.52
    a = None
    bc = "periodic"  # "bounce-back"

    def __init__(self, res, boundary_condition="periodic"):
        self.res = res
        self.bc = boundary_condition
        self._field = Field2D(self.res)
        self.velocityField=[]
        for DummyVariable in range(self.res):
            DummyList=[]
            for DummyVariable2 in range(self.res):
                DummyList.append([0,0])
            self.velocityField.append(DummyList[:])
        self.DensityField=[]
        for DummyVariable in range(self.res):
            DummyList=[]
            for DummyVariable2 in range(self.res):
                DummyList.append(1)
            self.DensityField.append(DummyList[:])

        self.a = Field2D(self.res)


    def step(self):
        # Collision Step
        df=Field2D(self.res)
        for y in range(self.res):
            for x in range(self.res):
                for v in range(9):
                    Velocity=self.a.field[y][x][v]
                    FirstTerm=Velocity
                    # The Flow Velocity
                    FlowVelocity=self.velocityField[y][x]
                    Dotted=FlowVelocity[0]*self.DiscreteVelocityVectors[v][0]+FlowVelocity[1]*self.DiscreteVelocityVectors[v][1]
                    # #The taylor expainsion of equilibrium term
                    taylor=1+((Dotted)/(self.SpeedOfSound**2))+((Dotted**2)/(2*self.SpeedOfSound**4))-((FlowVelocity[0]**2+FlowVelocity[1]**2)/(2*self.SpeedOfSound**2))
                    # The current density
                    density=self.DensityField[y][x]
                    # The equilibrium
                    equilibrium=density*taylor*self.Weights[v]
                    SecondTerm=(equilibrium-Velocity)/self.TimeRelaxationConstant
                    df.field[y][x][v]=FirstTerm+SecondTerm
        # Streaming Step
        # bc = "periodic"
        # bc = "bounce-back"
        for y in range(0,self.res):
            for x in range(0,self.res):
                for v in range(9):
                    # Target, the lattice point this iteration is solving
                    TargetY=y+self.DiscreteVelocityVectors[v][1]
                    TargetX=x+self.DiscreteVelocityVectors[v][0]
                    if self.bc == "periodic":
                        # Periodic Boundary
                        if TargetY == self.res and TargetX == self.res:
                            self.a.field[TargetY-self.res][TargetX-self.res][v]=df.field[y][x][v]
                        elif TargetX == self.res:
                            self.a.field[TargetY][TargetX-self.res][v]=df.field[y][x][v]
                        elif TargetY == self.res:
                            self.a.field[TargetY-self.res][TargetX][v]=df.field[y][x][v]
                        elif TargetY == -1 and TargetX == -1:
                            self.a.field[TargetY+self.res][TargetX+self.res][v]=df.field[y][x][v]   
                        elif TargetX == -1:
                            self.a.field[TargetY][TargetX+self.res][v]=df.field[y][x][v]
                        elif TargetY == -1:
                            self.a.field[TargetY+self.res][TargetX][v]=df.field[y][x][v]
                        else:
                            self.a.field[TargetY][TargetX][v]=df.field[y][x][v]
                    elif self.bc == "bounce-back":
                        # Bounce Back Boundary Conditions
                        vv = [8,7,6,5,4,3,2,1,0]
                        if TargetY == self.res and TargetX == self.res:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetX == self.res:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetY == self.res:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetY == -1 and TargetX == -1:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetX == -1:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetY == -1:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        else:
                            self.a.field[TargetY][TargetX][v] = df.field[y][x][v]
        # Calculate macroscopic variables
        for y in range(self.res):
            for x in range(self.res):
                # Recompute Density Field
                self.DensityField[y][x]=sum(self.a.field[y][x])
                # Recompute Flow Velocity
                FlowVelocity=[0,0]
                for DummyVariable in range(9):
                    FlowVelocity[0]=FlowVelocity[0]+self.DiscreteVelocityVectors[DummyVariable][0]*self.a.field[y][x][DummyVariable]
                for DummyVariable in range(9):
                    FlowVelocity[1]=FlowVelocity[1]+self.DiscreteVelocityVectors[DummyVariable][1]*self.a.field[y][x][DummyVariable]
                FlowVelocity[0]=FlowVelocity[0]/self.DensityField[y][x]
                FlowVelocity[1]=FlowVelocity[1]/self.DensityField[y][x]
                # Insert to Velocity Field
                self.velocityField[y][x]=FlowVelocity


class LB(Scene):

    res=40

    def construct(self):
        # periodic or bounce-back
        lb1 = _LB(self.res, boundary_condition="bounce-back")
        grid1 = self.vis(None, lb1.a, lb1.velocityField)
        grid1.shift(LEFT*3.3)
        lb2 = _LB(self.res, boundary_condition="periodic")
        grid2 = self.vis(None, lb2.a, lb2.velocityField)
        grid2.shift(RIGHT*3.3)

        lb1.DensityField[round(self.res/3.0)][round(self.res/2.0)] = 2.5
        lb2.DensityField[self.res - round(self.res/3.0)][round(self.res/2.0)] = 2.5

        self.wait(1)
        for i in range(128):
            lb1.step()
            lb2.step()
            grid1 = self.vis(grid1, lb1.a, lb1.velocityField)
            grid2 = self.vis(grid2, lb2.a, lb2.velocityField)
            if i > 10:
                # unset the density value
                lb1.DensityField[5][25] = 1
                lb2.DensityField[5][25] = 1
                self.wait(0.1)
            else:
                self.wait(0.3)


    def vis(self, grid, a, velocityField):
        ft = True
        if grid is None:
            #grid = Square().get_grid(self.res,self.res,height=6, buff=.2).set_stroke(width=0)
            grid = Circle().get_grid(self.res,self.res,height=6, buff=.6).set_stroke(color=WHITE, width=0)
            #grid = RegularPolygon(6).get_grid(self.res,self.res,height=6, buff=.2).set_stroke(width=0)
            
            ft = False
        ma = 0
        for y in range(self.res):
            for x in range(self.res):
                c = a.Momentum(x,y,velocityField)
                c = math.sqrt(c[0]**2+c[1]**2)
                ma = max(ma,c)
        if ma == 0:
            ma = 1
        # setup a colormap
        cm = color_gradient([BLACK, BLUE_A], 256)
        for i in range(self.res*self.res):
            c = a.Momentum(i//self.res,i%self.res,velocityField)
            c = math.sqrt(c[0]**2+c[1]**2)/ma
            #if c > 1:
            #    c = .1

            #col = '#%02x%02x%02x' % (int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2))) 
            col = cm[int(255*c)]
            grid[i].set_fill(col,1)
            x, y = i//self.res - self.res/2, i%self.res - self.res/2
            if math.sqrt(x**2 + y**2) >= self.res/2:
                grid[i].set_opacity(0.1)
        #self.wait(.1)
        if not(ft):
            self.add(grid)
        return grid
```