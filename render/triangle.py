from .base.base import BaseRender
import itertools
from numpy import arange


class Triangle(BaseRender):
    def __init__(self, points, colors):
        super().__init__(points, colors)
        self.x_min_max, self.y_min_max = self.get_min_max()
        self.direction = 1

    def render(self):
        p_min_x = self.points[self.x_min_max[0]]  # [x, y]
        p_max_x = self.points[self.x_min_max[1]]  # [x, y]
        p_min_y = self.points[self.y_min_max[0]]  # [x, y]
        p_max_y = self.points[self.y_min_max[1]]  # [x, y]

        # opacity=1
        # count=0
        for x in arange(int(p_min_x[0]-1), int(p_max_x[0]+1), 1):
            opacity=1
            for y in arange(int(p_min_y[1]-1), int(p_max_y[1]+1), 0.5):
                if  self.ray_tracing(x,y):
                    BaseRender.draw_pixel([x,y], self.colors[0])




        # for x in arange(int(p_min_x[0]), int(p_max_x[0])+1, 1):
            # for y in arange(int(p_min_y[1]), int(p_max_y[1])+1, 0.25):
                # print(count)
                # count+=1
                # if count == 3:
                    # print(count)
                    # if opacity != 0:
                        # BaseRender.draw_pixel([x,y], [i*opacity for i in self.colors[0]])
                    # opacity=1
                    # count=0
                    # continue
                # if not self.ray_tracing(x,y):
                    # opacity-=.25

    @staticmethod
    def inside_all(all_combinations, check_point):
        for points in all_combinations:
            is_inside = Triangle.inside(points[0], points[1], check_point)
            if not is_inside:
                return False
        return True

    def ray_tracing(self, x, y):
        # if (self.pointOnBorder(x, y) == True):
            # return True

        n = len(self.points)
        inside = False
        p2x = 0.0
        p2y = 0.0
        xints = 0.0
        p1x, p1y = self.points[0]
        for i in range(n+1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def pointOnBorder(self, x, y):
        n = len(self.points)
        for i in range(n):
            p1x, p1y = self.points[i]
            p2x, p2y = self.points[(i + 1) % n]
            v1x = p2x - p1x
            v1y = p2y - p1y  # vector for the edge between p1 and p2
            v2x = x - p1x
            v2y = y - p1y  # vector from p1 to the point in question
            if(v1x * v2y - v1y * v2x == 0):  # if vectors are parallel
                if(v2x / v1x > 0):  # if vectors are pointing in the same direction
                    if(v1x * v1x + v1y * v1y >= v2x * v2x + v2y * v2y):  # if v2 is shorter than v1
                        return True
        return False

  
    def get_min_max(self):
        x_min_max=[0,0] # [min, max]
        y_min_max=[0,0] # [min, max]
        for i in range(len(self.points)):
            if (i == 0):
                y_min_max[1] = i
            if (self.points[i][1] > self.points[y_min_max[1]][1]):
                y_min_max[1] = i
            elif (self.points[i][1] < self.points[y_min_max[0]][1]):
                y_min_max[0] = i
            if (self.points[i][0] > self.points[x_min_max[1]][0]):
                x_min_max[1] = i
            elif (self.points[i][0] < self.points[x_min_max[0]][0]):
                x_min_max[0] = i
        return [x_min_max, y_min_max]
