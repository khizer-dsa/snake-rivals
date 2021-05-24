				Snake Rivals

OVERVIEW
Snake Rivals is an updated version of the classic snake game which includes two snakes; one is the user snake which is controlled by the user through the keyboard and the other one is a bot snake which runs automatically using breadth-first search (BFS) and the Dijkstra’s algorithm to find the shortest route to the food. We will be calling the user snake as ‘snake’ and the bot snake as ‘worm’. Basically, the snake and worm try to reach the food and whoever eats it first scores a point.

REQUIREMENTS
* Python 
* pygame module should be installed
* Fonts and images that are in the zip folder


USAGE
Run 'snake-khizer.py' file to play the game.
To control the user snake and the main menu,  a keyboard is used.
* Snake : Navigate the snake’s movement through ↑, ↓, ←, → keys or W, A, S and D keys.
* Worm: To find worm’s next moving direction, D, the bot snake follows the steps below:
   1. Navigates the multiple possibilities for the worm’s head to reach the apple by implementing Breadth-first Search (BFS).
   2. Traverses along the shortest path from the worm’s head to the apple’s location via Dijkstra’s Algorithm. This generates the direction D.
   3. The worm moves along direction D.
* Main Menu/Game Over Screen: 
   1. Press ‘Enter’ to Start.
   2. Press ‘↓’ then press ‘Enter’  to Quit.
* Game Screen:
   1. Press ‘Esc’ to terminate the game.
   2. Press ‘p’ to pause the game.
   3. Press ‘u’ to unpause the game.
  

Green snake = snake (user)
Red and green snake = worm (auto-snake)

MODALITIES
1. The Snake and Worm must not touch the boundaries. Failing to do so will lead to the ‘Game Over’ screen.
2. The Snake and Worm must not touch each other. Failing to do so will lead to the ‘Game Over’ screen.
3. The Snake and Worm must not touch themselves. Failing to do so will lead to the ‘Game Over’ screen.
4. For every apple the snake/worm eats, the length of the snake/worm extends by 1 cell size.
5. Each player’s score is equal to the number of apples eaten since the start of the game.


Data Structures Used:
1. Queues
2. Dictionary
3. Breadth-first search (BFS) 
4. Dijkstra
5. Graphs



References:
[1] https://github.com/memoiry/Snaky/blob/master/snaky_ai_v2.py (worm bfs)
[2] https://www.sourcecodester.com/tutorials/python/11784/python-pygame-simple-main-menu-selection.html (main menu)
[3] https://www.youtube.com/watch?v=--nsd2ZeYvs (tutorial)
[4] https://www.pygame.org/docs/tut/newbieguide.html
[5] https://www.pygame.org/docs/ref/pygame.html (pygame documentation)
