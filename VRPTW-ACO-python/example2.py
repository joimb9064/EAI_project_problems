from vrptw_base import VrptwGraph
from basic_aco import BasicACO

if __name__ == '__main__':
    file_path = '/Users/josephimbien/Desktop/EAI_projects/eai_project_problems/VRPTW-ACO-python/solomon-100/c102.txt'
    ants_num = 10
    max_iter = 200
    beta = 3
    q0 = 0.1
    alpha = 1.0  # Add the alpha parameter here
    Q = 1.0  # Add the Q parameter here
    show_figure = True
    
    # Include Q in the VrptwGraph constructor
    graph = VrptwGraph(file_path, Q=Q)
    
    # Include alpha in the BasicACO constructor
    basic_aco = BasicACO(graph, ants_num=ants_num, max_iter=max_iter, alpha=alpha, beta=beta, q0=q0, cost_of_violation=100,
                         whether_or_not_to_show_figure=show_figure)

    # Run the ACO algorithm
    basic_aco.run_basic_aco()
    basic_aco.cost_of_violation = 500  # this will affect all Ant objects
    # Now, you can access the ants from the BasicACO object
    ants = basic_aco.ants

    # If you want to continue moving the ants around, you can do so like this:
    for i in range(max_iter):
        for ant in ants:
            # Define next_index for each ant and each iteration
            next_index = basic_aco.select_next_index(ant)  # compute next_index here
            ant.move_to_next_index(next_index, i)  # Pass the iteration number to the function

    # After all ants have finished moving, write to CSV
    ants[0].write_to_csv()