import solara
from model import ElFarolModel
from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component
)

def agent_portrayal(agent):
    return {
        "Shape": "circle",
        "Color": "red" if agent.attend else "white",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5
    }

model_params = {
    "seed":{ # user can input a random seed for reproducibility
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "N": { # user can adjust the number of agents
        "type": "SliderInt",
        "value": 100,
        "label": "Number of Agents",
        "min": 100,
        "max": 1000,
        "step": 10
    },
    "num_strategies": { # user can adjust the initial density of infected agents
        "type": "SliderInt",
        "value": 5,
        "label": "Number of Strategies",
        "min": 1,
        "max": 10,
        "step": 1
    },
    "memory_size": { # user can enable or disable vaccination
        "type": "SliderInt",
        "value": 5,
        "label": "Memory Size",
        "min": 1,
        "max": 10,
        "step": 1
    },
    "overcrowding_threshold": { # user can adjust the probability of transmission
        "type": "SliderFloat",
        "value": 0.6,
        "label": "Overcrowding Threshold",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05
    },
}

elfarolmodel = ElFarolModel()
elfarolspace = make_space_component(elfarolmodel, agent_portrayal)

# define the Solara page with the model and components
page = SolaraViz(
    elfarolmodel,
    components=[elfarolspace],
    model_params=model_params,
    name="El Farol Model"
)
## return page
page
