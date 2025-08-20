*Code adapted from [this NetLogo implementation](https://ccl.northwestern.edu/netlogo/models/ElFarol) of the original Arthur (1994) El Farol model.*

# El Farol Bar Problem

This directory contains an implementation of Arthur's (1994) model of the El Farol Bar problem. In the model, agents are members of the town of El Farol who enjoy spending time at the local dive bar. However, there's nothing the citizens of El Farol like less than a night at the bar when it is crowded. As a rule of thumb, El Farolians enjoy the bar when less than 60% of the town population is enjoying the bar with them. If over 60% of the population is at the bar on a given night, everyone in attendance ends up having less fun than they would have if they'd stayed home and read a book on the couch. Agents use a variety of strategies, aided by their memories of their enjoyment of the bar at various fullness levels, to predict whether, on a given night, the bar will be too crowded for their liking. Their decision to attend depends on this prediction.

## Suggestions for implementation in MACSS 40550

This model will give students a chance to play around with different grid and space types in Mesa. There is also room for students to play around with different parameters, both those that are included in this model and others, like changing the overcrowding threshold. Honestly, this probably isn't a great model to have student recreate for class, but could be a good example to show when exploring GUIs.

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.