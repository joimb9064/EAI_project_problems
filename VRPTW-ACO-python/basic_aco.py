import numpy as np
import random
from vprtw_aco_figure import VrptwAcoFigure
from vrptw_base import VrptwGraph, PathMessage
from ant import Ant
from threading import Thread
from queue import Queue
import time
import csv
import datetime
import os


class BasicACO:
    def __init__(self, graph: VrptwGraph, ants_num=10, max_iter=100, alpha=1.0, beta=2, q0=0.1,
                 whether_or_not_to_show_figure=True, cost_of_violation=100):
        super()
        self.alpha = alpha
        self.graph = graph
        self.ants_num = ants_num
        self.max_iter = max_iter
        self.max_load = graph.vehicle_capacity
        self.beta = beta
        self.q0 = q0
        self.best_path_distance = None
        self.best_path = None
        self.best_vehicle_num = None
        self.ants = None  # Initialize ants
        self.basicACO_results = []  # Initialize results attribute 
        self.cost_of_violation = cost_of_violation  # Cost of violation
        self.whether_or_not_to_show_figure = whether_or_not_to_show_figure
        self.terminate_program = False  # Termination flag

    def run_basic_aco(self):
        path_queue_for_figure = Queue()
        basic_aco_thread = Thread(target=self._basic_aco, args=(path_queue_for_figure,))
        basic_aco_thread.start()
        if self.whether_or_not_to_show_figure:
            figure = VrptwAcoFigure(self.graph.nodes, path_queue_for_figure)
            figure.run()
        basic_aco_thread.join()

        if self.whether_or_not_to_show_figure:
            path_queue_for_figure.put(PathMessage(None, None))

    def _basic_aco(self, path_queue_for_figure: Queue):
        start_time_total = time.time()
        start_iteration = 0
        global results
        results = []

        for iter in range(self.max_iter):
            if self.terminate_program:  # Check termination flag
                print("Program termination requested. Exiting after current iteration.")
                break

            self.ants = [Ant(self.graph, cost_of_violation=self.cost_of_violation) for _ in range(self.ants_num)]
            for k in range(self.ants_num):
                next_index = 0
                self.ants[k].move_to_next_index(next_index, iter, self.best_vehicle_num)
                self.graph.local_update_pheromone(self.ants[k].current_index, next_index, 0)  # No penalty for depot

                while not self.ants[k].index_to_visit_empty():
                    next_index = self.select_next_index(self.ants[k])
                    if not self.ants[k].check_condition(next_index):
                        next_index = self.select_next_index(self.ants[k])
                        if not self.ants[k].check_condition(next_index):
                            next_index = 0

                    penalty = self.ants[k].calculate_penalty(next_index)
                    self.ants[k].move_to_next_index(next_index, iter, self.best_vehicle_num)
                    self.graph.local_update_pheromone(self.ants[k].current_index, next_index, penalty)

                self.ants[k].move_to_next_index(0, iter, self.best_vehicle_num)
                self.graph.local_update_pheromone(self.ants[k].current_index, 0, 0)  # No penalty for depot

            paths_distance = np.array([ant.total_travel_distance for ant in self.ants])

            best_index = np.argmin(paths_distance)
            if self.best_path is None or paths_distance[best_index] < self.best_path_distance:
                self.best_path = self.ants[int(best_index)].travel_path
                self.best_path_distance = paths_distance[best_index]
                self.best_vehicle_num = self.best_path.count(0) - 1
                start_iteration = iter

                self.basicACO_results.append({
                    'Iteration': iter,
                    'Improved path distance': self.best_path_distance,
                    'Iteration path': ', '.join(map(str, self.best_path)),
                    'Execution time': round(time.time() - start_time_total, 3),
                    'Total travel distance': round(self.best_path_distance, 2),
                    'Number of vehicles used': self.best_vehicle_num
                })

                if self.whether_or_not_to_show_figure:
                    path_queue_for_figure.put(PathMessage(self.best_path, self.best_path_distance))

                print('\n[iteration %d]: found an improved path, distance is %f' % (iter, self.best_path_distance))
                print('The iteration path is: ', self.best_path)
                print('it takes %0.3f seconds ant_colony_system running' % (time.time() - start_time_total))

            self.graph.global_update_pheromone(self.best_path, self.best_path_distance)

            given_iteration = 100
            if iter - start_iteration > given_iteration:
                print('Exiting: No better solution found in %d iterations' % given_iteration)
                break

        self.write_basicACO_to_csv(self.basicACO_results)
        self.ants[0].write_to_csv()

        print('\nFinal best path distance is %f, number of vehicles is %d' % (self.best_path_distance, self.best_vehicle_num))
        print('The best path is: ', self.best_path)
        print('it takes %0.3f seconds ant_colony_system running' % (time.time() - start_time_total))

    def write_basicACO_to_csv(self, basicACO_results):
        csv_dir = "/Users/josephimbien/desktop/EAI_project_problems/VRPTW-ACO-python/csv"
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d-%H-%M-%S")
        csv_path = os.path.join(csv_dir, f'basicACO_results_{now_str}.csv')

        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ['Iteration', 'Improved path distance', 'Iteration path', 'Execution time', 'Total travel distance', 'Number of vehicles used']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in basicACO_results:
                writer.writerow(result)

    def select_next_index(self, ant):
        current_index = ant.current_index
        index_to_visit = ant.index_to_visit

        if len(index_to_visit) == 0:
            #print("No more nodes to visit. Flagging for termination.") # Turn this on for debugging but by default it should be off.
            self.terminate_program = True  # Set the termination flag
            return 0  # Return to depot or terminate this ant's tour

        penalties = np.array([ant.calculate_penalty(i) for i in index_to_visit])
        heuristic_with_penalty = np.array([self.graph.calculate_heuristic_with_penalty(current_index, i) for i in index_to_visit])

        transition_prob = np.power(self.graph.pheromone_mat[current_index][index_to_visit], self.alpha) * \
                          np.power(self.graph.heuristic_info_mat[current_index][index_to_visit], self.beta)

        if np.sum(transition_prob) == 0:
            print("No valid transition probabilities. Flagging for termination.")
            self.terminate_program = True  # Set the termination flag
            return 0  # Return to depot or terminate this ant's tour

        transition_prob = transition_prob / np.sum(transition_prob)

        if np.random.rand() < self.q0:
            max_prob_index = np.argmax(transition_prob)
            next_index = index_to_visit[max_prob_index]
        else:
            next_index = BasicACO.stochastic_accept(index_to_visit, transition_prob)

        return next_index

    @staticmethod
    def stochastic_accept(index_to_visit, transition_prob):
        if len(index_to_visit) == 0:
            return 0  # Return to depot or terminate

        N = len(index_to_visit)
        sum_tran_prob = np.sum(transition_prob)
        if sum_tran_prob == 0:
            return 0  # Handle the termination or depot return

        norm_transition_prob = transition_prob / sum_tran_prob
        while True:
            ind = int(N * random.random())
            if random.random() <= norm_transition_prob[ind]:
                return index_to_visit[ind]
