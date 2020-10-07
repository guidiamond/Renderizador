from .base.base import BaseRender


class Point(BaseRender):
    def __init__(self, points, colors):
        super().__init__(points, colors)

    def render(self):
        for i in range(len(self.points)):
            BaseRender.draw_pixel(self.points[i], self.colors[i])
