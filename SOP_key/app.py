import solara
from model import SOPModel
from agents import AudienceMember
from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component
)

# agents are portrayed as blue squares if standing and red squares if sitting
def agent_portrayal(agent):
    return {
        "color": "blue" if agent.standing else "red",
        "marker": "s",
        "size": 40,
    }

# create a plot component to visualize the proportion of agents acting against their instinct
InstinctPlot = make_plot_component("proportion_against_instinct")

# define model parameters for the Solara interface
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "neighbor_structure": {
        "type": "Select",
        "value": "five",
        "label": "Neighbor Structure",
        "values": AudienceMember.neighbor_structure,
    },
    "update": {
        "type": "Select",
        "value": "Sync",
        "label": "Update Order",
        "values": SOPModel.update_order,
    }
}

# create the space component to visualize the grid of agents
space = make_space_component(agent_portrayal=agent_portrayal)
sop_model = SOPModel()

# create the Solara page with the model, space, and plot components
page = SolaraViz(
    model=sop_model,
    model_params=model_params,
    components=[space, InstinctPlot],
    name="Standing Ovation Problem",
)
## return page
page