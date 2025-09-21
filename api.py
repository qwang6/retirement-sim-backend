from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import json # Import json module for pretty printing

# Assuming simulation.py is in the same directory or accessible via PYTHONPATH
from simulation import run_simulation

# Create the FastAPI app instance
app = FastAPI(
    title="Retirement Simulator API",
    description="An API to run Monte Carlo retirement simulations.",
    version="1.0.0",
)

# --- Pydantic Data Models ---

class SimulationInput(BaseModel):
    """
    Defines the structure and validation for the simulation inputs coming from the client.
    """
    initial_portfolio_value: float = Field(1000000, gt=0, description="The starting value of your investment portfolio.")
    initial_cost_basis: float = Field(700000, gt=0, description="The original value of your assets for tax purposes.")
    annual_spending: float = Field(120000, gt=0, description="The total amount of money you plan to spend annually.")
    monthly_passive_income: float = Field(1000, ge=0, description="Monthly passive income.")
    portfolio_annual_return: float = Field(0.10, description="The expected average annual return of your portfolio.")
    portfolio_annual_std_dev: float = Field(0.19, gt=0, description="The annualized standard deviation of portfolio returns (volatility).")
    quarterly_dividend_yield: float = Field(0.01, ge=0, description="Quarterly dividend yield.")
    margin_loan_annual_avg_interest_rate: float = Field(0.06, description="The average annual interest rate on your margin loan.")
    margin_loan_annual_interest_rate_std_dev: float = Field(0.015, ge=0, description="The standard deviation of the margin loan interest rate.")
    brokerage_margin_limit: float = Field(0.50, gt=0, lt=1, description="The maximum percentage of your portfolio you are willing to borrow on margin.")
    federal_tax_free_gain_limit: int = Field(123250, gt=0, description="Federal tax-free gain limit for harvesting.")
    tax_harvesting_profit_threshold: float = Field(0.30, gt=0, description="The unrealized profit percentage that triggers tax-gain harvesting.")
    num_simulations: int = Field(1000, gt=0, le=5000, description="The number of different market scenarios to simulate.")
    
    # Advanced settings for distribution models
    return_distribution_model: str = Field('Normal', pattern="^(Normal|Student's t|Laplace)$")
    return_distribution_df: float = Field(5, gt=2, description="Degrees of Freedom for Student's t distribution (returns).")
    interest_rate_distribution_model: str = Field('Normal', pattern="^(Normal|Student's t|Laplace)$")
    interest_rate_distribution_df: float = Field(5, gt=2, description="Degrees of Freedom for Student's t distribution (interest rates).")

class SimulationOutput(BaseModel):
    """
    Defines the structure for the simulation results sent back to the client.
    """
    max_net_worth: List[float]
    avg_net_worth: List[float]
    min_net_worth: List[float]

# --- API Endpoint ---

@app.post("/simulate", response_model=SimulationOutput)
async def create_simulation(inputs: SimulationInput) -> SimulationOutput:
    """
    Runs the retirement simulation based on the provided input parameters.
    """
    # Convert the Pydantic model to a dictionary for the simulation function
    inputs_dict = inputs.dict()
    print(f"[API] Received inputs: {json.dumps(inputs_dict, indent=2)}")
    
    # Run the core simulation logic
    results, _ = run_simulation(inputs_dict)
    print(f"[API] Raw simulation results keys: {results.keys()}")
    print(f"[API] Length of avg_net_worth: {len(results['avg_net_worth']) if 'avg_net_worth' in results else 'N/A'}")
    
    # Convert numpy arrays to standard Python lists for JSON serialization
    response_data = {
        'max_net_worth': results['max_net_worth'].tolist(),
        'avg_net_worth': results['avg_net_worth'].tolist(),
        'min_net_worth': results['min_net_worth'].tolist(),
    }
    print(f"[API] Prepared response data keys: {response_data.keys()}")
    print(f"[API] Length of prepared avg_net_worth: {len(response_data['avg_net_worth'])}")
    
    return SimulationOutput(**response_data)