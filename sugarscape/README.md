*Code adapted from MACSS 40550 repository, which itself is based on the Mesa Examples version of Sugarscape*

# SugarScape with Reproduction

This directory contains an implementation of Epstein and Axtell's (1996) model SucarScape from the book *Growing Artifical Societies*, in which agents attempt to survive in an environment defined by the distribution of sugar, a resource they need to survive. Agents vary in how far they can see on the map and how much sugar they require to stay alive. The model is a canonical attempt to to grow a society from the ground up in a specific spatial context, with emergent outcomes like inequality (tracked here as the Gini index over agents' sugar endowments) and carrying capacity.

In this version of the model, consumed sugar grows back at a rate of one unit per time step from an initial defined spatial distribution, instantiated in the text file in this directory. Agents move to the closest available spot within their vision that maximizes their potential to consume sugar, and die if they ever have zero or negative sugar.

The model also implements functionality to mimic agent reproduction. Reproduction depends upon the fertility of a pair of agents, which itself is determined by the agent's sugar holdings and age. If two agents are fertile and of the opposite sex, they will produce an offspring that is endowed with half of each parent's sugar holdings and a random combination of their features.

## Suggestions for implementation in MACSS 40550

You can provide students with the base code already utilized in the MACSS 40550 repository. From there, students can choose to add functionality based on one of the chapters of SugarScape (ie. reproduction, trading, combat).

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.
