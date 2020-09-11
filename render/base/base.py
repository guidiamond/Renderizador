import gpu
class BaseRender():
    def __init__(self, points, colors):
        self.points, self.colors = BaseRender.formatter(points, colors)
        self.u1=self.points[0][0]
        self.v1=self.points[0][1]
        if (len(self.points) >= 2):
            self.u2=self.points[1][0]
            self.v2=self.points[1][1]
        self.sign_y = 1
        self.sign_x = 1

    @staticmethod
    def draw_pixel(points, colors):
        return gpu.GPU.set_pixel(int(points[0]), int(points[1]), colors[0], colors[1], colors[2])

    @staticmethod
    def formatter(points, colors):
        formated_points = []
        formatted_colors = []
        i=0
        n_iterations = len(points) // 2
        for e in range(n_iterations):
            formated_points.append([points[i], points[i+1]])
            formatted_colors.append([i*255 for i in colors])
            i+=2
        return [formated_points, formatted_colors]
