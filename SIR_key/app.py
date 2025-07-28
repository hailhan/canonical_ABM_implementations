import solara
from model import SIRModel
from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component
)

def sir_agent_portrayal(agent):
    return {
        "color": "yellow" if agent.state == 'S' else "red" if agent.state == 'I' else "purple",
        "marker": "s",
        "size": 10,
    }

SusceptiblePlot = make_plot_component("num_susceptible")
InfectedPlot = make_plot_component("num_infected")
RecoveredPlot = make_plot_component("num_recovered")

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
    },
    "infected_density": {
        "type": "SliderFloat",
        "value": 0.1,
        "label": "Initial Infected Density",
        "min": 0.0,
        "max": 1.0,
        "step": 0.1
    },
    "vaccination": {
        "type": "Checkbox",
        "value": False,
        "label": "Enable Vaccination",
    }
}

sir_model = SIRModel()
sir_space = make_space_component(agent_portrayal=sir_agent_portrayal)

page = SolaraViz(
    sir_model,
    components=[sir_space, SusceptiblePlot, InfectedPlot, RecoveredPlot],
    model_params=model_params,
    name="SIR Model"
)
## return page
page
