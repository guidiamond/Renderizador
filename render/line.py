from .base.base import BaseRender

class Line(BaseRender):
    def __init__(self,points,colors):
        super().__init__(points, colors)

    def get_slope(self):
        x1,y1 = self.points[0]
        x2,y2 = self.points[1]
        dx=x2-x1
        dy=y2-y1
        if (dx == 0):
            return ['v',dx, dy]
        if (dy == 0):
            return ['h',dx, dy]
        slope = dy/dx
        return [ slope, dx, dy ]


    @staticmethod
    def finished_plotting(delta, u1, u2):
        if (delta < 0):
            return u1 > u2
        return u1 < u2

    def draw_horizontal(self, delta):
        number_of_pixels=round(abs(delta))
        for e in range(0,number_of_pixels):
            BaseRender.draw_pixel([self.u1, self.v1], self.colors[0])
            self.u1+=self.sign_x

    def draw_vertical(self, delta):
        number_of_pixels=round(abs(delta))-1
        for e in range(0,number_of_pixels):
            BaseRender.draw_pixel([self.u1, self.v1], self.colors[0])
            self.v1+=self.sign_y


    @staticmethod
    def get_signs(dx,dy):
        sign_x = 1
        sign_y = 1
        if (dx < 0):
            sign_x = -1
        if (dy < 0):
            sign_y = -1
        return [sign_x, sign_y]

    def bresenham_alg(self, dx, dy, flip=False):
        p = (2*abs(dy)) - abs(dx)
        while (Line.finished_plotting(dx, self.u1, self.u2)):
            BaseRender.draw_pixel([self.u1, self.v1], self.colors[0])
            self.u1+= self.sign_x
            if (p<0):
                p=p+2*abs(dy)
            else:
                p=p+2*(abs(dy)-abs(dx))
                self.v1+=  self.sign_y
        BaseRender.draw_pixel([self.u2, self.v2], self.colors[0])

    def bresenham_alg_inv(self, dx, dy):
        p = (2*abs(dx)) - abs(dy)
        while (Line.finished_plotting(dy, self.v1, self.v2)):

            BaseRender.draw_pixel([self.u1, self.v1], self.colors[0])
            self.v1+=  self.sign_y
            if (p<0):
                p=p+2*abs(dx)
            else:
                p=p+2*(abs(dx)-abs(dy))
                self.u1+=  self.sign_x

        BaseRender.draw_pixel([self.u2, self.v2], self.colors[0])


    def render(self):

        """
        steps:
        1 => get slope, dx, dy
        2 => if (dx|dy) < 0 then it's going backwards (-1 instead of +1)
        3 => check which axis to do the base (which is bigger) sampling (which will always increase by one)
        4 => apply bresenham algorithm
        """
        # step 1
        slope, dx, dy = self.get_slope()


        # step 2
        self.sign_x, self.sign_y = Line.get_signs(dx,dy)
        if (str(slope) == 'h'):
            self.draw_horizontal(dx)
            return
        elif (str(slope) == 'v'):
            self.draw_vertical(dy)
            return
        # step 3
        if (abs(dx) > abs(dy)):
            #step 4
            self.bresenham_alg(dx,dy)
        else:
            self.bresenham_alg_inv(dx,dy)

