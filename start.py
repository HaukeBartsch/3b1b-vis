from manimlib import *

class Anim(Scene):
    def construct(self):
        square = Square()
        square.set_z(0)
        square.set_fill(BLUE, 1)

        circle = Circle()
        circle.set_fill(ORANGE, 1)
        circle.set_stroke(width=0)
        circle.set_z(0)
        circleSmall = circle.copy()
        circleSmall.set_fill(BLACK)
        circleSmall.set_z(0)
        circleSmall.scale(0.2)
        CD = VGroup( circle, circleSmall )

        self.play(FadeIn(square))
        self.wait()
        self.play(VGroup(circle, circleSmall, square).animate.shift(2 * LEFT))
        self.wait()
        square.set_z(.05)
        # new location should old location but with shift in x only
        self.play(square.animate.scale(1.1),
                  CD.animate.set_z(0).shift(4 * RIGHT),
                  square.animate.scale(0.9))
        self.wait()


class Data(Scene):
    def construct(self):
        alpha_tracker = ValueTracker(0.0)
        axes_start = Axes((-5, 25, 5), (0,3), height= FRAME_HEIGHT - 2)
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
        self.play(alpha_tracker.animate.set_value(1.0), run_time=4)

        #
        # After we have the summary we can create one more graph for another measure.
        # We need to move the graph down and create a new graph.
        #

        axes1 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, tips=False)
        axes2 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, tips=False)
        axes3 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, tips=False)
        axes4 = Axes((-5, 25, 5), (0,2), height= FRAME_HEIGHT/8, tips=False)
        axes5 = Axes((-5, 25, 5), (0,3), height= FRAME_HEIGHT/8, tips=False)

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

