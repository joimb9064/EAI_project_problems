import matplotlib.pyplot as plt
from multiprocessing import Queue as MPQueue


class VrptwAcoFigure:
    def __init__(self, nodes: list, path_queue: MPQueue):
        self.nodes = nodes
        self.figure = plt.figure(figsize=(10, 10))
        self.figure_ax = self.figure.add_subplot(1, 1, 1)
        self.path_queue = path_queue
        self._depot_color = 'k'
        self._customer_color = 'steelblue'
        self._line_color = 'darksalmon'

    def _draw_point(self):
        self.figure_ax.scatter([self.nodes[0].x], [self.nodes[0].y], c=self._depot_color, label='depot', s=40)
        self.figure_ax.scatter(list(node.x for node in self.nodes[1:]),
                               list(node.y for node in self.nodes[1:]), c=self._customer_color, label='customer', s=20)
        plt.pause(0.5)

    def run(self):
        self._draw_point()
        self.figure.show()

        while True:
            if not self.path_queue.empty():
                info = self.path_queue.get()
                while not self.path_queue.empty():
                    info = self.path_queue.get()
            # Retrieve penalty from info , 30 September 2024.
                path, distance, used_vehicle_num , penalty = info.get_path_info()
                if path is None:
                    print('[draw figure]: exit')
                    break

                lines_to_remove = [line for line in self.figure_ax.lines if line.get_label() == 'line']
                for line in lines_to_remove:
                    line.remove()  # Remove line from axes
            # Include penalty in the title , 30 September 2024.
                self.figure_ax.set_title('travel distance: %0.2f, number of vehicles: %d, penalty: %0.2f' % (distance, used_vehicle_num, penalty))
                self._draw_line(path)
            plt.pause(1)

    def _draw_line(self, path):
        for i in range(1, len(path)):
            x_list = [self.nodes[path[i - 1]].x, self.nodes[path[i]].x]
            y_list = [self.nodes[path[i - 1]].y, self.nodes[path[i]].y]
            self.figure_ax.plot(x_list, y_list, color=self._line_color, linewidth=1.5, label='line')
            plt.pause(0.2)