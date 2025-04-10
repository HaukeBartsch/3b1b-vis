from manimlib import *

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

# Pseudonymization
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


# FIONA's role
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