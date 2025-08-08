import solara
from model import ForestFireModel
from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component
)


def ff_agent_portrayal(agent):
    # agents will be represented as circles with different colors indicating fire state
    return {
        "color": "green" if agent.state == 'Tree' 
        else "orange" if agent.state == 'Burning' 
        else "black", # empty state is black
        "marker": "s",
        "size": 100,
    }

# create plot components for the model reporters
BurnedPropPlot = make_plot_component(
    "burned_prop")    

# define model parameters for the Solara interface
model_params = {
    "p": {
        "type": "SliderFloat",
        "value": 0.6,
        "label": "Tree Density",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05
    },
    "width": {
        "type": "SliderInt",
        "value": 10,
        "label": "Forest Width",
    },
    "height": {
        "type": "SliderInt",
        "value": 10,
        "label": "Forest Height",
    }
}

ff_model = ForestFireModel()
ff_space = make_space_component(agent_portrayal=ff_agent_portrayal)

# define the Solara page with the model and components
page = SolaraViz(
    ff_model,
    components=[ff_space, BurnedPropPlot],
    model_params=model_params,
    name="Forest Fire Model"
)
## return page
page