# GalagaAI


## Introduction
We aim to develop an agent that is capable of effectively playing the game Galaga.  The agent will be in control of a spaceship in a boxed, continuous environment.  

Galaga is a non-turn-based video game that consists of a single player agent and several enemies that spawn indefinitely until the game is over. The objective of the game is to dodge incoming projectiles from enemies while simultaneously launching projectiles at enemies to destroy them and achieve the highest possible score. 


## Design Diagrams

### Context
Below is a high level overview of the system architecture.  The evaluator is a person that continously evaluates the agent's performance from a visual perspective through a viewer.  Internally, the Viewer retains performance data as the agent plays its game and outputs it to the evaluator.  The state of the environment is continously recorded and simultaneously outputted to the agent.

![alt text](/docs/Context.png)


### Container
The below diagram further breaks down the interactions between the self contained items within the Alien Invasion application.  Both the agent and training controller can exist individually without an Alien Invasion game, but rely on data from the environment to be useful.  Both the controller and agent are further described in later sections.

![alt text](/docs/Container.png)