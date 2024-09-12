def evaluate_solution(ant, penalty_factor=1000):
    # Calculate the total travel distance and time window violations
    total_distance = ant.total_travel_distance
    time_window_violations = ant.time_window_violations
    
    # Combine these metrics into a single objective value
    objective_value = total_distance + (time_window_violations * penalty_factor)
    
    return objective_value