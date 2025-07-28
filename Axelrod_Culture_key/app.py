import solara
from model import CultureModel
from mesa.visualization import (
    SolaraViz,
    make_space_component,
    make_plot_component
)

def culture_to_color(features):
    # assigns a unique color to each unique culture (combination of features)
    key = tuple(features)  # make features hashable (ie. immutable)
    hash_val = abs(hash(key))  # make sure key is positive
    r = (hash_val >> 0) % 256
    g = (hash_val >> 8) % 256
    b = (hash_val >> 16) % 256
    return f'#{r:02x}{g:02x}{b:02x}'

def agent_portrayal(agent):
    # agents will be rectangles with color based on their features
    return {
        "color": culture_to_color(agent.features),
        "shape": "rect",
        "w": 1,
        "h": 1,
    }

# create a plot component for model reporters
RegionPlot = make_plot_component("region_counts")

# define model parameters for solara
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    }
}

# initialize model and space component for visualization
culture_model = CultureModel()
culture_space = make_space_component(agent_portrayal=agent_portrayal)

# define the Solara page with the model and components
page = SolaraViz(
    culture_model,
    components=[culture_space, RegionPlot],
    model_params=model_params,
    name="Culture Model"
)
# return page
page