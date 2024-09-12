# main script
from vrptw_base import VrptwGraph
from multiple_ant_colony_system import MultipleAntColonySystem

if __name__ == '__main__':
    file_path = '/Users/josephimbien/Desktop/EAI_projects/eai_project_problems/VRPTW-ACO-python/solomon-100/c101.txt'
    ants_num = 10
    beta = 3
    q0 = 0.5
    show_figure = True

    graph = VrptwGraph(file_path)
    
    # Generate time_windows from graph nodes
    time_windows = [(node.ready_time, node.due_time) for node in graph.nodes]
    
    # Use distance matrix as initial travel_times
    travel_times = graph.node_dist_mat
    
    macs = MultipleAntColonySystem(graph=graph, time_windows=time_windows, travel_times=travel_times, ants_num=ants_num, beta=beta, q0=q0, whether_or_not_to_show_figure=show_figure)
    
    # Run the multiple ant colony system
    macs.run_multiple_ant_colony_system()

    # Evaluate solutions for each ant
    best_objective_value = float('inf')
    best_solution = None

    for ant in macs.ants:
        objective_value = macs.evaluate_solution(ant)
        print(f"Ant {ant} - Objective Value: {objective_value}")
        
        # Calculate time window violations
        violations = macs.calculate_time_window_violations(ant.travel_path)
        print(f"Time Window Violations: {violations}")
        
        if objective_value < best_objective_value:
            best_objective_value = objective_value
            best_solution = ant.travel_path

    print(f"Best Objective Value: {best_objective_value}")
    print(f"Best Solution: {best_solution}")

# multiple_ACO.py
# ... (rest of the code) ...
    @staticmethod
    def evaluate_solution(ant, penalty_factor=1000):
        # Calculate the total travel distance and time window violations
        total_distance = ant.total_travel_distance
        time_window_violations = ant.calculate_time_window_violations()  # updated
        
        # Combine these metrics into a single objective value
        objective_value = total_distance + (time_window_violations * penalty_factor)
        
        return objective_value

    def calculate_time_window_violations(self, route):
        violations = 0
        current_time = 0
        
        for i in range(len(route) - 1):
            current_location = route[i]
            next_location = route[i + 1]
            
            # Calculate arrival time at the next location
            current_time += self.travel_times[current_location][next_location]
            
            # Check if arrival time is within the time window
            start_time, end_time = self.time_windows[next_location]
            if current_time < start_time or current_time > end_time:
                violations += 1
                print(f"Violation at location {next_location}: current_time={current_time}, time_window=({start_time}, {end_time})")
            
            # Update current time to the maximum of arrival time and start of the time window
            current_time = max(current_time, start_time)
        
        return violations
# ... (rest of the code) ...