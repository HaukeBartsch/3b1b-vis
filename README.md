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

## Sum-of Gaussian distributions

Given a distribution of regional brain volumes for a cohort I wanted to display how that distribution can composed out of individual shifted and scaled distributions. A given probablity for regional brain volume and a related distance from the mean is therefore composed of different distances and probabilities in the underlying covariate distributions. Here I wanted to decompose the regional brain volume by age (young and old) and gender (male and female).

![DVD](https://github.com/HaukeBartsch/3b1b-vis/blob/main/videos/Data.gif)

This actually worked out ok. I was quite happy with this.

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