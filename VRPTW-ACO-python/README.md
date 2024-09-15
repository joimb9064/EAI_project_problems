# Ant Colony Optimization
A **python** implementation of a **ant colony optimization** based solution to **Vehicle Routing Problem with Time Windows**.


## Example

<p align="center">
	<img src="/VRPTW-ACO-python/image/c101-example.gif">
</p>


## How to Run the Python Code Sample:

Before starting, ensure that you have Python installed on your system. The code was tested with Python 3.6, but it should work with other 3.x versions as well.

1) **Clone the Repository:** Open your terminal or command prompt and run the following command to clone the repository:
```
gh repo clone joimb9064/EAI_project_problems
```

**Another way** of cloning this is using the "Github Desktop".


2) **Navigate to the Directory:** Change your current directory to the cloned repository. You can do this with the `cd` command:
```
cd VRPTW-ACO-python
```



3) **Change the `file_path` Variable:** If you are going to run the code on your own computer, you need to change the `file_path` variable to the path where your `c101.txt` file is located. When running the code, it is recommended to create your own Python script file. Instead of using `example1.py`, create a new `.py` file in the same directory and write your code in that file. This will allow you to make modifications and run your own experiments without altering the original code.

For instance, you might create a file named `my_script.py`. 

For example, your `main.py` script might contain the following lines:
```
if name == 'main': 
file_path = '/Users/josephimbien/Desktop/EAI_projects/eai_project_problems/VRPTW-ACO-python/solomon-100/c101.txt' 
ants_num = 10
```



4) **Run the Code:** You can now run the Python scripts. For example, to run `example1.py`, use the following command:
```
python example1.py
```

5) **Vitualization:** Download the html file in the html folder, then upload the csv file you wish to be processed from the csv folder of this project. Here are the exceptions applied in the html file. The file contains a lot of data, which for example
   A)The iterations where the Ants were not completed yet in converging a specific path. So the "Nodes Visited" here is set to minimum of 99 nodes.
   B) Applied Penalty is also present in the html functionality but literaly not displaying anything as of now since the Ants are very good in avoiding delivery after "Due Time".
   C) Which Vehicle Delivers on which "Customer No." or node can also be seen as part of the functionality of the post-processing html.
   



