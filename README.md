#Infexion AI Project - README

This repository contains the implementation of an AI agent for playing the game of Infexion. The project aims to develop an intelligent agent capable of making strategic decisions and playing the game effectively.

Game Description

Infexion is a two-player game with a set of predefined rules. It involves placing tokens on a hexagonal grid and spreading their influence to adjacent cells. The goal is to control the majority of the board by the end of the game. Please refer to the 'Rules for the Game of Infexion' document (v1.1) for a detailed understanding of the game mechanics.

Project Structure

The project consists of the following components:

Agent Program: The agent program is responsible for making decisions based on the current game state and selecting appropriate actions.
Referee Program: The referee program coordinates the game between two agent programs, enforces the game rules, and maintains the game state.
Running the Program

To run the agent program and play a game of Infexion, execute the referee program alongside the agent module. The referee program orchestrates the game and ensures fair gameplay. It provides a testing environment for immediate feedback on the agent's performance.

Please follow the instructions below to run the program:

Download and extract the project code from the repository.
Open a terminal and navigate to the project's root directory.
Run the following command: python -m referee agent agent
This command initiates a game between two instances of the agent program. Please note that the game will not work initially, as the agent's behavior needs to be implemented. This setup allows you to test your work locally. It is recommended to periodically test in the online environment provided by Gradescope, as it includes a simple opponent for your agent to compete against.

Agent Program Structure

The agent module contains a template Python 3.10 program that serves as a starting point for implementing the agent program. It defines a class named Agent, which must include the following methods:

__init__(self, color: PlayerColor, **referee: dict): This method initializes the agent at the beginning of the game and sets up the internal game state representation.
action(self, **referee: dict) -> Action: This method is called at the start of the agent's turn to select and return the desired action based on the current game state.
turn(self, color: PlayerColor, action: Action, **referee: dict): This method is called at the end of each player's turn to update the agent's internal game state representation.
You can modify and extend these methods to implement your game-playing strategy and decision-making process.

Representing Actions

Actions in the game are represented using dataclass definitions provided in the actions.py file in the referee/game directory. Please refer to this file to understand how to construct actions based on the game rules and specifications.

Program Constraints

During testing, the following resource limits will be enforced for each player's agent program:

Maximum computation time: 180 seconds per player, per game.
Maximum memory usage: 250MB per player, per game (excluding imported libraries).
Please ensure that your agent program adheres to these constraints and does not attempt to circumvent them.

