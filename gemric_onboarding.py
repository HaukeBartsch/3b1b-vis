from manimlib import *
# see https://mmiv.no/how-to-join-gemric/
# Still missing pauses
# arrow between lines could be done together (after move up)

class GEMRIC_new_site(Scene):
    def construct(self):
        #square = Square()
        #square.set_z(0)
        #square.set_fill(BLUE, 1)
        t = VGroup(
            Text(r"Site PI", font_size=32),
            Text(r"registers", font_size=32),
            Text(r"a new site", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT)
        #t.move_to(square.get_center())
        pi = VGroup(t)
        self.play(Write(pi))

        self.play(pi.animate.move_to(LEFT * 1.8))

        arrow = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow.next_to(pi, RIGHT)
        self.play(Write(arrow))

        square2 = Square()
        square2.set_fill(GREEN_D, 1)
        t2 = VGroup(
            Text(r"Inquiry form", font_size=28),
            Text(r"(~5min)", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT)
        t2.move_to(square2.get_center())
        g2 = VGroup( t2)
        g2.next_to(arrow, RIGHT)
        self.play(Write(g2))

        # move everything to the left
        self.play(
            VGroup(pi, arrow, g2).animate.shift(LEFT * 4)
        )

        arrow2 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow2.next_to(g2, RIGHT)
        self.play(Write(arrow2))

        square3 = Square()
        square3.set_fill(GREEN_D, 1)
        t3 = VGroup(
            Text(r"GEMRIC Review", font_size=22),
            Text(r"Any concerns?", font_size=22),
            Text(r"IRB initiated?", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT)
        t3.move_to(square3.get_center())
        g3 = VGroup(square3, t3)
        g3.next_to(arrow2, RIGHT)
        self.play(Write(g3))

        # sign data sharing agreement, fill out site info spreadsheet
        arrow3 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow3.next_to(g3, RIGHT)
        t5 = Text(r"", font_size=26)
        t5.move_to(arrow3).shift(UP*0.3)
        self.play(Write(VGroup(arrow3, t5)))
        t4 = VGroup(
            Text(r"Sign data sharing agreement", font_size=26),
            Text(r"and fill out site info spreadsheet", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT)
        t4.next_to(arrow3, RIGHT)
        self.play(Write(t4))

        #arrow35 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        #arrow35.next_to(t4, RIGHT)
        #self.play(Write(arrow35))

        # move everything up
        self.play(
            VGroup(pi, arrow, g2, arrow2, g3, arrow3, t5, t4).animate.shift(UP * 2)
        )

        # move this next bit down
        arrow4 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow4.move_to(LEFT * 6 + DOWN * 0.8)
        self.play(Write(arrow4))

        square4 = Square()
        square4.set_fill(GREEN, 1)
        t6 = VGroup(
            Text(r"Upload data", font_size=26),
            Text(r"instructions", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT)
        t6.move_to(square4.get_center())
        g4 = VGroup(square4, t6)
        g4.next_to(arrow4, RIGHT)
        self.play(Write(g4))

        arrow5 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow5.next_to(g4, RIGHT)
        self.play(Write(arrow5))

        t7 = VGroup(
            Text(r"Upload clinical data", font_size=24),
            Text(r"Upload MRI data", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT)
        t7.next_to(arrow5, RIGHT)
        self.play(Write(t7))

        arrow6 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow6.next_to(t7, RIGHT)
        self.play(Write(arrow6))

        square5 = Square()
        square5.set_fill(GREEN_D, 1)
        t7 = VGroup(
            Text(r"Convert IDs", font_size=20),
            Text(r"Import to REDCap", font_size=20),
            Text(r"Process T1 data", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT)
        t7.move_to(square5.get_center())
        g5 = VGroup(square5, t7)
        g5.next_to(arrow6, RIGHT)
        self.play(Write(g5))

        arrow7 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow7.next_to(g5, RIGHT)
        self.play(Write(arrow7))

        t8 = VGroup(
            Text(r"Check and confirm", font_size=26),
            Text(r"data quality", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT)
        t8.next_to(arrow7, RIGHT)
        self.play(Write(t8))

        # don't we need elevation to full membership, access to all data?
        arrow8 = Arrow(start=LEFT, end=RIGHT).scale(0.5)
        arrow8.move_to(DOWN * 3 + LEFT * 6)
        self.play(Write(arrow8))

        s = Rectangle(width=5, height=1.5)
        s.set_fill(GREEN, 1)
        t9 = VGroup(
            Text(r"Verified member with access to all data.", font_size=26),
            Text(r"Data can be part of new release.", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT)
        t9.move_to(s.get_center())
        g6 = VGroup(s, t9).next_to(arrow8, RIGHT)
        self.play(Write(VGroup(s,t9)))
