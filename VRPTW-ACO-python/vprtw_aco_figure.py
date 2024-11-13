import matplotlib.pyplot as plt
from multiprocessing import Queue as MPQueue
import os
import datetime

class VrptwAcoFigure:
    def __init__(self, nodes: list, path_queue: MPQueue):
        self.nodes = nodes
        self.figure = plt.figure(figsize=(10, 10))
        self.figure_ax = self.figure.add_subplot(1, 1, 1)
        self.path_queue = path_queue
        self._depot_color = 'k'
        self._customer_color = 'steelblue'
        self._line_color = 'darksalmon'
        self.best_distance = float('inf')  # Initialize the best distance to a very high value
        self.best_path_info = None  # To store the best path's info

    def _draw_point(self):
        self.figure_ax.scatter([self.nodes[0].x], [self.nodes[0].y], c=self._depot_color, label='depot', s=40)
        self.figure_ax.scatter(list(node.x for node in self.nodes[1:]),
                               list(node.y for node in self.nodes[1:]), c=self._customer_color, label='customer', s=20)
        plt.pause(0.01)

    def run(self):
        self._draw_point()
        plt.pause(0.01)

        while True:
            try:
                # Wait for a short time for an item to appear in the queue
                info = self.path_queue.get(timeout=10)  # Wait for 10 seconds for new data
                if info is None:
                    print('[draw figure]: exit')
                    break

                # Retrieve info from queue
                path, distance, used_vehicle_num, penalty = info.get_path_info()

                # Update only if this is the best path so far
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path_info = (path, distance, used_vehicle_num, penalty)  # Update best path info

                # Clear the old lines from the figure
                lines_to_remove = [line for line in self.figure_ax.lines if line.get_label() == 'line']
                for line in lines_to_remove:
                    line.remove()

                # Update the plot title with the path info
                self.figure_ax.set_title(
                    'Travel Distance: %.2f, Vehicles: %d, Penalty: %.2f' % 
                    (distance, used_vehicle_num, penalty)
                )
                self._draw_line(path)

                plt.pause(0.01)

            except Exception as e:
                print("Timeout or queue is empty, exiting loop.")
                break  # Exit the loop if no data is received

        # After the loop ends, save the final best path
        if self.best_path_info:
            self._save_final_best_path()

    def _save_final_best_path(self):
        path, distance, used_vehicle_num, penalty = self.best_path_info

        # Save the figure with date and time in the filename
        output_dir = "/Users/josephimbien/Desktop/unitesting Problem 3 ACO/VRPTW-ACO-python/image"
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get current time for the filename
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Set the plot title to include the final best path
        self.figure_ax.set_title(
            'Final Best Path - Travel Distance: %.2f, Vehicles: %d, Penalty: %.2f' % 
            (distance, used_vehicle_num, penalty)
        )

        # Save the plot with the date and time in the filename
        output_file_path = os.path.join(output_dir, f"final_best_path_distance_{distance:.2f}_vehicles_{used_vehicle_num}_{current_time}.png")
        self.figure.savefig(output_file_path, format='png')  # Save the plot as .png
        print(f"Successfully saved final best path as: {output_file_path}")
        print("Exiting gracefully after saving the final best path.")

        # Exit the figure loop cleanly to prevent further updates
        plt.close(self.figure)

    def _draw_line(self, path):
        for i in range(1, len(path)):
            x_list = [self.nodes[path[i - 1]].x, self.nodes[path[i]].x]
            y_list = [self.nodes[path[i - 1]].y, self.nodes[path[i]].y]
            self.figure_ax.plot(x_list, y_list, color=self._line_color, linewidth=1.5, label='line')
            plt.pause(0.01)
