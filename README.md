# Monte Carlo Retirement Simulation

This project is a Python-based Monte Carlo simulation model to assess the viability of a specific retirement plan over a 10-year period.

## Project Overview

The simulation models a retirement strategy where an individual with a $1M stock portfolio plans to live by borrowing on margin against it, rather than selling shares for income. The model simulates the interaction between portfolio growth, living expenses, margin loan interest, quarterly dividends, and an annual tax-gain harvesting strategy.

The final output shows the monthly range of potential net worth (maximum, average, and minimum) across thousands of simulated market scenarios, helping to quantify the risk and potential success of this strategy.

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/Retirement-Sim.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd Retirement-Sim
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Simulation

This project offers two ways to run the simulation:

### 1. Interactive Web Interface (Recommended)

For an interactive experience where you can easily change the input parameters and visualize the results, use the Gradio web application.

To start the web interface, run the following command:
```bash
python3 app.py
```
This will launch a local web server. Open the URL displayed in your terminal (e.g., `http://127.0.0.1:7860`) in your browser to access the application.

### 2. Command-Line Simulation

To run the simulation directly from the command line with the default parameters, execute:
```bash
python3 simulation.py
```
The script will output a results table to the console and display a plot visualizing the simulation outcomes.

## Customizing the Simulation

-   **Via the Web Interface**: The easiest way to customize the simulation is by running `app.py` and modifying the inputs directly in your browser.
-   **Via the Command-Line**: If you are using `simulation.py`, you can customize the run by modifying the `inputs` dictionary within the `main()` function of the script.

## Project Files

-   `app.py`: A web-based, interactive UI for the simulation built with Gradio. (Recommended)
-   `simulation.py`: The core Python script for the Monte Carlo simulation. Can be run directly.
-   `requirements.txt`: A list of the Python packages required for the project.
-   `README.md`: This file.
-   `ref/project_idea.md`: The project plan and requirements specification.
-   `ref/info.html`: An HTML file with a UI for the simulation.
