# Maze Game
#### Video Demo:  <https://youtu.be/0c3hQ38e_Xg>
This is a maze game implemented in Python using the Pygame library. The objective of the game is to navigate a player through a maze to reach the end point.

## How to Play

1. **Controls**:
   - Use the arrow keys (Up, Down, Left, Right) to move the player, all at the same speed.
   - The speed is predeteremined within the code.

2. **Game Elements**:
   - Walls: Represented by black blocks, the player cannot pass through walls.
   - Player Character: You control a player that can move through open spaces (The white background).
   - End Point: Your goal is to reach the end point (marked with a purple square) to win the game.
   - When end goal is reached the game will end and close the program.

3. **Game Rules**:
   - The player character cannot move through walls.
   - If the player character collides with a wall, they cannot pass through it.
   - When the player character reaches the end point, the game ends, and you win.

## Code Description
How it was created.

1.**Background/world**:

The program initially started with just a background, inspired by a platformer game. This background consisted of full black rectangle tiles surrounding a filled white section. This evolved to include walls all around the screen based on 1s in "world_data" variable.

2.**Player**:

The player was then created using just a green square in the middle of the screen. This progressed into movement using the arrow keys on a keyboard. With the movement of the player created a collision issue. Originally the character could move through any of the black walls. Using the built in collide function this was then stopped.

3.**End goal**:

When a maze design and a player was completed there needed to be an indicator for the end point of the maze. Using an image generater created a purple tile that when collided with finished the program.

4.**With additional time**

Optionally could create:
- Play multiple levels all with different maze designs.
- Create a timer from start to finish
- Create a vision definition where the user could only see a few tiles around them to make the level harder.
