from mesa.batchrunner import batch_run
from model import SOPModel
import csv

# Define parameters to sweep
params = {
    "width": 20,
    "height": 20,
    "neighbor_structure": ["five", "cones"],  # Example neighbor structures
    "update": ["Sync", "AsyncRandom", "AsyncIncentive"],  # Different update orders
    "seed": [1, 10, 25],  # Random seeds for reproducibility
}

if __name__ == '__main__':
    # Run batch simulations with the defined parameters
    results = batch_run(
        SOPModel,
        parameters=params,
        max_steps=200,  # Maximum number of steps for each run
        number_processes=8,  # Number of parallel processes to use
        display_progress=True,  # Show progress bar
        data_collection_period=1,  # Collect data every step
        iterations=100,  # Number of iterations for each parameter combination
    )
    
    # Write results to a CSV file
    with open("batch_results.csv", mode="w", newline="") as f:
       writer = csv.DictWriter(f, fieldnames=results[0].keys())
       writer.writeheader()
       for row in results:
            writer.writerow(row)