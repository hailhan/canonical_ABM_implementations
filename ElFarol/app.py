## ADD BAR BOUNDARIES IF POSSIBLE
import solara
from mesa.visualization import SolaraViz, make_space_component
from model import ElFarolModel  # your model file

def ef_agent_portrayal(agent):
    return {
        "color": "red" if agent.attend 
        else "blue",
        "marker": "^", # triangle agents
        "size": 15,
    }

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "N": {
        "type": "SliderInt",
        "value": 100,
        "label": "Number of Agents",
        "min": 100,
        "max": 1000,
        "step": 10,
    },
    "num_strategies": {
        "type": "SliderInt",
        "value": 5,
        "label": "Number of Strategies",
        "min": 1,
        "max": 10,
        "step": 1,
    },
    "memory_size": {
        "type": "SliderInt",
        "value": 5,
        "label": "Memory Size",
        "min": 1,
        "max": 10,
        "step": 1,
    },
}

efmodel= ElFarolModel()
# Create space visualization component
elfarolspace = make_space_component(
    agent_portrayal=ef_agent_portrayal)

# Create SolaraViz page, using the model class and parameters
page = SolaraViz(
    efmodel,
    components=[elfarolspace],
    model_params=model_params,
    name="El Farol Model",
)
# Render page
page