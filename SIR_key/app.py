import solara
from model import SIRModel
from mesa.visualization import (
    SolaraViz,
    make_space_component
)

def sir_agent_portrayal(agent):
    #print(f"Rendering agent at {agent.pos} with state {agent.state}")
    return {
        "color": "yellow" if agent.state == 'S' else "red" if agent.state == 'I' else "purple",
        "marker": "s",
        "size": 10,
    }

model_params = {
    "seed":{
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "infection_duration": {
        "type": "SliderInt",
        "value": 7,
        "label": "Infection Duration (days)",
        "min": 1,
        "max": 14,
        "step": 1
    }
} # add a checkbox for vaccinations

sir_model = SIRModel()
sir_space = make_space_component(agent_portrayal=sir_agent_portrayal)

page = SolaraViz(
    sir_model,
    components=[sir_space],
    model_params=model_params,
    name="SIR Model"
)
## return page
page
