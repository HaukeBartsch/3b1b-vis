from manimlib import *

# Create an animation about the data in image data (travel to the moon)
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

