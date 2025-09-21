import pytest
from pydantic import ValidationError

# We assume api.py is in the same directory or accessible
from api import SimulationInput

def test_valid_simulation_input():
    """ Tests successful creation of SimulationInput with valid data. """
    valid_data = {
        'initial_portfolio_value': 1000000,
        'initial_cost_basis': 700000,
        'annual_spending': 120000,
        'portfolio_annual_return': 0.10,
        'portfolio_annual_std_dev': 0.19,
        'quarterly_dividend_yield': 0.01,
        'margin_loan_annual_avg_interest_rate': 0.06,
        'margin_loan_annual_interest_rate_std_dev': 0.015,
        'brokerage_margin_limit': 0.50,
        'tax_harvesting_profit_threshold': 0.30,
        'num_simulations': 1000,
    }
    try:
        instance = SimulationInput(**valid_data)
        assert instance.initial_portfolio_value == 1000000
        print("✅ TC-1.1a: Valid data successfully created a SimulationInput instance.")
    except ValidationError as e:
        pytest.fail(f"Valid data failed validation: {e}")

def test_invalid_simulation_input():
    """ 
    Tests that SimulationInput raises a ValidationError with invalid data.
    Here, initial_portfolio_value is negative, which should fail the gt=0 constraint.
    """ 
    invalid_data = {
        'initial_portfolio_value': -100, # Invalid value
        'initial_cost_basis': 700000,
        'annual_spending': 120000,
        'portfolio_annual_return': 0.10,
        'portfolio_annual_std_dev': 0.19,
        'quarterly_dividend_yield': 0.01,
        'margin_loan_annual_avg_interest_rate': 0.06,
        'margin_loan_annual_interest_rate_std_dev': 0.015,
        'brokerage_margin_limit': 0.50,
        'tax_harvesting_profit_threshold': 0.30,
        'num_simulations': 1000,
    }
    with pytest.raises(ValidationError):
        SimulationInput(**invalid_data)
    print("✅ TC-1.1b: Invalid data correctly raised a ValidationError.")

if __name__ == "__main__":
    # A simple runner without needing the full pytest framework
    try:
        test_valid_simulation_input()
        test_invalid_simulation_input()
        print("\n🎉 All model tests passed! Pydantic models are correctly defined.")
    except Exception as e:
        print(f"❌ A test failed: {e}")
