*Model implementation is based on the description provided in PA1 from MACSS 30111/30121*

# The SIR Model

This is a model of the spread of infection through a community. The model can be run with or without the presence of vaccines. In the model, agents can have one of three states: susceptible, infected, and recovered (and additionally vaccinated when vaccines are enabled). Susceptible agents are at risk of becoming infected if any of their neighbors are also infected. The infection will last a consistent duration (which can be modified by the user), and once the infection has run its course the agent will be recovered and cannot become susceptible/infected again. The user can also manipulate the initial density of infected agents in the population.

## Suggestions for implementation in MACSS 40550

Students who have taken the MACSS 30111/30121 course will already be familiar with the SIR model. This assignment could provide them an opportunity to approach the SIR with Mesa/object-oriented programming. I would recommend providing the students with the [PA1 description from MACSS 30111/121](https://classes.ssd.uchicago.edu/macss/macs30121/modules/pa/pa1.html) to work from- tell them to only focus on the description of the model elements, not the actual implementation suggestions. *NOTE: must be on campus wifi/VPN in order for the link to work!* I would recommend encouraging students to use their imagination with this model: they can add functionality like variant infection duration in a single model run, a recovered/immune state that can wear off after a period of time to allow for reinfection, or other such details.

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.