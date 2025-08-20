# Axelrod's Culture Model

This directory contains the relevant files to run an implementation of Axelrod's (1997) "Dissemination of Culture Model". In the model, agents are stationary dots that represent communities. Each community is initialized with a unique "culture" comprised of 5 features, each of which has a random integer value from 1 to 10. In each model step, agents interact with their neighbors if they share any of their five features. When an agent interacts with a neighboring agent, they adopt one of the neighbor's features with a probability equal to the similarity between the agents (ie. two agents with two identical features have a similarity of 40%). As the model progresses, regions of cultural similarity begin to emerge as neighbors become more similar over time and therefore more likely to interact.

## Suggestions for implementation in MACSS 40550

The basic functionality of this model is incredibly simple, so it will be easy for students to implement while gaining familiarity with Mesa. The challenge for this model is in its representation. There are too many potential combinations of "cultures" for students to use a simple color scheme to visualize their differences. A hash table is used to generate different colors for different cultures in this implementation of the model, but there are probably other creative ways to visualize cultural dissemination. This model will therefore give students a chance to dig in to the app functionality to make a compelling model visualization. Additionally, the model will force students to think about how to define and calculate model reporters. 

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.