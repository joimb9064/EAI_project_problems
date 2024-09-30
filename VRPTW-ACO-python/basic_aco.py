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
        # Add the alpha parameter to the class
        self.alpha = alpha
        self.graph = graph
        self.ants_num = ants_num
        self.max_iter = max_iter
        self.max_load = graph.vehicle_capacity
        self.beta = beta
        self.q0 = q0
        # best path
        self.best_path_distance = None
        self.best_path = None
        self.best_vehicle_num = None
        self.ants = None  # Add this line to initialize the ants attribute
        self.basicACO_results = []  # Add this line to initialize the basicACO_results attribute 
        # 30 September, added to minimize the phermone to routes with Penalties
        self.cost_of_violation = cost_of_violation  # Add this line 
        self.whether_or_not_to_show_figure = whether_or_not_to_show_figure

    def run_basic_aco(self):
        path_queue_for_figure = Queue()
        basic_aco_thread = Thread(target=self._basic_aco, args=(path_queue_for_figure,))
        basic_aco_thread.start()
        if self.whether_or_not_to_show_figure:
            figure = VrptwAcoFigure(self.graph.nodes, path_queue_for_figure)
            figure.run()
        basic_aco_thread.join()
        # Call the method here

        if self.whether_or_not_to_show_figure:
            path_queue_for_figure.put(PathMessage(None, None))

    def _basic_aco(self, path_queue_for_figure: Queue):
        start_time_total = time.time()
        start_iteration = 0
        # Clear the results list at the start of each run
        global results
        results = []
        # 30 September, added to minimize the phermone to routes with Penalties
        for iter in range(self.max_iter):
            self.ants = list(Ant(self.graph, cost_of_violation=self.cost_of_violation) for _ in range(self.ants_num))
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
         # 30 September, added to minimize the phermone to routes with Penalties
                # Only append the result if the next_index is a depot
                if self.graph.nodes[next_index].is_depot:
                    results.append(results)

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

                print('\n')
                print('[iteration %d]: find a improved path, its distance is %f' % (iter, self.best_path_distance))
                print('The iteration path is: ', self.best_path)  # Print the best path
                print('it takes %0.3f second multiple_ant_colony_system running' % (time.time() - start_time_total))

            self.graph.global_update_pheromone(self.best_path, self.best_path_distance)

            given_iteration = 100
            if iter - start_iteration > given_iteration:
                print('\n')
                print('iteration exit: can not find better solution in %d iteration' % given_iteration)
                break
        self.write_basicACO_to_csv(self.basicACO_results)
        self.ants[0].write_to_csv()
        
        print('\n')
        print('final best path distance is %f, number of vehicle is %d' % (self.best_path_distance, self.best_vehicle_num))
        print('The best path is: ', self.best_path)  # Print the best path
        print('it takes %0.3f second multiple_ant_colony_system running' % (time.time() - start_time_total))

    def write_basicACO_to_csv(self, basicACO_results):
        csv_dir = "/Users/josephimbien/desktop/EAI_project_problems/VRPTW-ACO-python/csv"  # specify your directory here
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d-%H-%M-%S")
        csv_path = os.path.join(csv_dir, f'basicACO_results_{now_str}.csv')

        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ['Iteration', 'Improved path distance', 'Iteration path', 'Execution time', 'Total travel distance', 'Number of vehicles used']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for basicACO_result in basicACO_results:
                writer.writerow(basicACO_result)
    def select_next_index(self, ant): # Update this part September.2024.
        """
        Select the next node
        :param ant:
        :return:
        """
        current_index = ant.current_index
        index_to_visit = ant.index_to_visit
        # 30 September, added to minimize the phermone to routes with Penalties
        # Calculate penalties for each potential next node
        penalties = np.array([ant.calculate_penalty(i) for i in index_to_visit])
        # 30 September, added to minimize the pheromone to routes with Penalties
        # Adjust heuristic information based on penalties
        heuristic_with_penalty = np.array([self.graph.calculate_heuristic_with_penalty(current_index, i) for i in index_to_visit])


        # Use self.alpha to adjust the importance of pheromone information
        transition_prob = np.power(self.graph.pheromone_mat[current_index][index_to_visit], self.alpha) * \
            np.power(self.graph.heuristic_info_mat[current_index][index_to_visit], self.beta)
        transition_prob = transition_prob / np.sum(transition_prob)

        if np.random.rand() < self.q0:
            max_prob_index = np.argmax(transition_prob)
            next_index = index_to_visit[max_prob_index]
        else:
            # Use roulette wheel selection algorithm
            next_index = BasicACO.stochastic_accept(index_to_visit, transition_prob)
        return next_index
    @staticmethod
    def stochastic_accept(index_to_visit, transition_prob):
        # calculate N and max fitness value
        N = len(index_to_visit)

        # normalize
        sum_tran_prob = np.sum(transition_prob)
        norm_transition_prob = transition_prob/sum_tran_prob

        # select: O(1)
        while True:
            # randomly select an individual with uniform probability
            ind = int(N * random.random())
            if random.random() <= norm_transition_prob[ind]:
                return index_to_visit[ind]
            
