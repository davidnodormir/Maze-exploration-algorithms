### Project Overview

This repository features a Python-based project developed for a University Artificial Intelligence course. The objective is to solve complex mazes using a variety of search strategies, ranging from **uninformed** and **informed** search to **local search** and **evolutionary algorithms**.

The project was a collaborative effort between three students. Together, we designed and implemented:

  * **Graphical User Interface (GUI):** A dynamic interface built with **Pygame** that visualizes the maze and the real-time progress of each algorithm.
  * **Maze Generation:** Logic for loading and parsing different maze structures from text files.
  * **Core Logic:** The shared infrastructure handling movement costs.
### My Contributions

While the core infrastructure was a team effort, each member focused on implementing specific search strategies. I personally developed:

1.  **Breadth-First Search (BFS):** An uninformed search strategy that explores all nodes at the current depth before moving to the next level, guaranteeing the shortest path in terms of steps.
2.  **Local Beam Search:** A heuristic-based variation of local search that tracks $k$ states (the "beam width") simultaneously, allowing for a more robust exploration of the state space compared to a standard hill-climbing approach.
3.  **Genetic Algorithm:** An evolutionary approach where a population of potential paths evolves over generations through **selection, crossover, and mutation** to find an optimal or near-optimal solution.

### How to Run

1.  **Requirements:** Ensure you have `pygame` installed (`pip install pygame`).
2.  Run the main script: `python [nome_del_file].py`.
3.  Enter the name of a maze file in the terminal  (or simply press **Enter** to load the default 3x3 maze).
4.  Select an algorithm from the side panel to see it in action\!

Eventually, you can build your own maze by using maze generator and choosing the size. I have included 2 default mazes, the first 3*3 and the other one 6*6. 

> [\!TIP]
> For an in-depth analysis of **time complexity** and algorithmic logic refer to the Documentation PDF

My favorite part of this project was conducting the **performance comparison** between the different algorithms. As a PC gamer, I have a natural love for stats and benchmarks\!
<img width="591" height="416" alt="immagine" src="https://github.com/user-attachments/assets/043eafc2-ae9d-4712-a46d-074646418d4a" />



