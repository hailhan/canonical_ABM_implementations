import solara
from model import CultureModel
from mesa.visualization import (
    SolaraViz,
    make_space_component
)

def culture_to_color(features):
    key = tuple(features)  # ensure it's hashable
    hash_val = abs(hash(key))  # make sure it's positive
    r = (hash_val >> 0) % 256
    g = (hash_val >> 8) % 256
    b = (hash_val >> 16) % 256
    return f'#{r:02x}{g:02x}{b:02x}'

def agent_portrayal(agent):
    return {
        "color": culture_to_color(agent.features),
        "shape": "rect",
        "w": 1,
        "h": 1,
    }

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    }
}

culture_model = CultureModel()
culture_space = make_space_component(agent_portrayal=agent_portrayal)

page = SolaraViz(
    culture_model,
    components=[culture_space],
    model_params=model_params,
    name="Culture Model"
)
# return page
page