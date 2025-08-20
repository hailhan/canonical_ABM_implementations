import solara
from model import SIRModel
from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component
)

def sir_agent_portrayal(agent):
    # agents will be represented as circles with different colors indicating disease state
    return {
        "color": "yellow" if agent.state == 'S' 
        else "red" if agent.state == 'I' 
        else "purple", # both "R" and "V" states are purple
        "marker": "s",
        "size": 50,
    }

# create plot components for the model reporters
SusceptiblePlot = make_plot_component("num_susceptible")
InfectedPlot = make_plot_component("num_infected")
RecoveredPlot = make_plot_component("num_recovered")

# define model parameters for the Solara interface
model_params = {
    "seed":{ # user can input a random seed for reproducibility
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "infection_duration": { # user can adjust the duration of infection
        "type": "SliderInt",
        "value": 7,
        "label": "Infection Duration (days)",
        "min": 1,
        "max": 14,
        "step": 1
    },
    "infected_density": { # user can adjust the initial density of infected agents
        "type": "SliderFloat",
        "value": 0.1,
        "label": "Initial Infected Density",
        "min": 0.0,
        "max": 1.0,
        "step": 0.1
    },
    "vaccination": { # user can enable or disable vaccination
        "type": "Checkbox",
        "value": False,
        "label": "Enable Vaccination",
    }
}

# initialize the model and space component for visualization
sir_model = SIRModel()
sir_space = make_space_component(agent_portrayal=sir_agent_portrayal)

# define the Solara page with the model and components
page = SolaraViz(
    sir_model,
    components=[sir_space, SusceptiblePlot, InfectedPlot, RecoveredPlot],
    model_params=model_params,
    name="SIR Model"
)
## return page
page
