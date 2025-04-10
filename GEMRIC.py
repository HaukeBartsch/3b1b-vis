from manimlib import *

# How is SAFE working, our data analysis system for international collaborations? 
# Safe is not actually a single system.
# Actually it is 2 systems, one Windows and one Linux virtual machine.
# We access the Windows system using Remote Desktop. Once inside the Windows system we can access the Linux system with an inside Remote Desktop.
# Our 2 systems have names inside Safe, for GEMRIC those are Henderson and Homlungen.

# How does data for processing reach our systems? Sending files with Remote Desktop to Henderson is not possible.
# Instead we need to use another transfer system called desktop. Uploading files to desktop is allowed.
# Such uploaded files placed in desktop's import folder are automatically transferred to Henderson.
# They disappear from desktop and appear 10min later in Henderson's import folder.


# show how we access the safe system
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