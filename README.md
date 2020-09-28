# Sudoku-App
Sudoku generator and solver gui in python



i created a sudoku generator and solver GUI!
i have implemented two algorithms to solve sudoku boards, one of them is the classic backtracking algorithm ,the second algorithm uses backtracking but also uses a heuristic
to take a more informed approach when trying to come up with an answer ,it uses a minimum value remaining heuristic 
meaning it tries to first fill cells that have less valid options that can be inserted in them.
i also have implemented a sudoku board generator that generates random and uniquely solvable boards.
The Graphical user interface was created using the pygame module.

the sudoku_solver.py script is the main script from which you can run the application

the gui has features such as showing you a visualization of how the algorithm is solving the board and many other features!!
