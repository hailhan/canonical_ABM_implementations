*Code based on [this version](https://rf.mokslasplius.lt/forest-fire-model/#Drossel1992PRL) of Drossel & Schwabl's (1992) Forest Fire Model.*

# Forest Fire Model

This directory contains an implementation of Drossel & Schwabl's (1992) Forest Fire model. In this version of the model, each agent represents a plot of land on which there can be nothing, a tree, or a burning tree. The central agent on the grid is always initialized as a burning tree. Each step, each tree agent looks at their Von Neumann neighbors to determine whether any are burning. If a neighboring tree is burning, that tree will start burning too. The model progresses in this fashion until no more trees catch fire, at which point the model stops.

## Suggestions for implementation in MACSS 40550

From a functional standpoint, this model is a much more simplified version of the SIR. As it is currently, it also lacks an explicit social science component. I recommend encouraging students to expand upon the basic functionality, to both create a more complex model and make connections to social scientific theory. For instance, students could incorporate human agents who evacuate burning areas to explore the relationship between climate change and human settlement patterns. There are a number of ways that students could build on this model, and I think it will be necessary for them to do so in order to make this model worthwhile for an assignment. 

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.