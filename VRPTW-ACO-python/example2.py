# Pheromone update has been applied if a node has encountered a violation.
# The ants should treat that node as low priority, since the phermone value will decrease which will cause the ants
# not to pass thru that path since the Pheromone value does not attract them.
# However, it does not add the penalty at the end of the "total cost".
# Should have a formula of "Total cost = Total Distance travel + Penalty". 
# Added BasicACO class logic to dump a csv file
# Added additional fields on the Ant Class to add fields like "Ready Time" and "Due Date", "End of Service minus Due date" and "Nodes Visited".
# Approved as completed project with Dung.
# Marked as complete September 30,2024.
#  Penalty is explicitly added in the output figure.
# Added additional parameter rho - evaporation rate

from vrptw_base import VrptwGraph
from basic_aco import BasicACO

if __name__ == '__main__':
    file_path = '/Users/josephimbien/Desktop/EAI_project_problems/VRPTW-ACO-python/solomon-100/R201.txt'
    ants_num = 10
    max_iter = 200
    beta = 3
    q0 = 0.2
    alpha = 0.2  # Add the alpha parameter here
    Q = 0.2  # Add the Q parameter here
    rho = 0.5  # Add the rho parameter here
    show_figure = True
    
    # Include Q and rho in the VrptwGraph constructor
    graph = VrptwGraph(file_path, rho=rho, Q=Q)
    
    # Include alpha in the BasicACO constructor
    basic_aco = BasicACO(graph, ants_num=ants_num, max_iter=max_iter, alpha=alpha, beta=beta, q0=q0, cost_of_violation=100,
                         whether_or_not_to_show_figure=show_figure)

    # Run the ACO algorithm
    basic_aco.run_basic_aco()
    basic_aco.cost_of_violation = 4000  # this will affect all Ant objects
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