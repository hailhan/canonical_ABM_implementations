# The Standing Ovation Problem

This directory contains the relevant files for a Mesa implementation of Miller & Page's Standing Ovation Problem (2007). This model imagines an audience directly after the conclusion of a performance. Each agent has an internal assessment of their enjoyment of the performance, which determines whether they will initially stand or sit for the applause. As the applause continues, will it evolve into a full standing ovation? This model operationalizes peer pressure as the mechanism driving standing ovations, with agents assessing how many fellow audience members within their field of vision are sitting/standing, and adjusting their behavior accordingly. This implementation reports on the proportion of agents acting against their initial instinct to estimate the influence of peer pressure on individual behavior.

## Suggestions for implementation in MACSS 40550

Students can build this model from scratch, based on pgs. 14-15 of the Miller & Page article already assigned in the syllabus. The challenge for this model is figuring out which model reporters to utilize, and how to incorporate them into the model datacollector. This would be a great opportunity for students to get comfortable with batch runs. Students should try to figure out how to measure IE, SIM, and NI through their batch runs.

## How to Run

To run the model interactively once you have a complete agents file, run the following code in this directory:

```
    $ solara run app.py
```

## Files

* ``agents.py``: Contains the agent class
* ``model.py``: Contains the model class
* ``app.py``: Defines classes for visualizing the model in the browser via Solara, and instantiates a visualization server.