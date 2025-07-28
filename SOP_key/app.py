import solara
from model import SOPModel
from agents import AudienceMember
from mesa.visualization import (
    SolaraViz,
    make_space_component
)

def agent_portrayal(agent):
    return {
        "color": "blue" if agent.standing else "red",
        "marker": "s",
        "size": 40,
    }

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

space = make_space_component(agent_portrayal=agent_portrayal)
sop_model = SOPModel()

page = SolaraViz(
    model=sop_model,
    model_params=model_params,
    components=[space],
    name="Standing Ovation Problem",
)
## Return page
page