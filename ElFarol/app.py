import solara
from mesa.visualization import SolaraViz, make_space_component
from model import ElFarolModel  # your model file

def ef_agent_portrayal(agent):
    return {
        "color": "red" if agent.attend else "blue",
        "marker": "^",
        "size": 15,  # smaller size
        "alpha": 0.6,  # semi-transparent if supported
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
    "overcrowding_threshold": {
        "type": "SliderFloat",
        "value": 0.6,
        "label": "Overcrowding Threshold",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
    },
    "width": {
        "type": "SliderInt",
        "value": 10,
        "label": "Grid Width",
        "min": 5,
        "max": 50,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 10,
        "label": "Grid Height",
        "min": 5,
        "max": 50,
        "step": 1,
    },
}

efmodel= ElFarolModel()
# Create the space visualization component with the model class and portrayal function
elfarolspace = make_space_component(agent_portrayal=ef_agent_portrayal)

# Create the SolaraViz page, using the model class and parameters
page = SolaraViz(
    efmodel,
    components=[elfarolspace],
    model_params=model_params,
    name="El Farol Model",
)

page