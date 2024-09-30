import json
import numpy as np
from forecasting_model import forecast_emissions
from optimization_algorithm import optimize_energy_usage

# Provide the AWS Lambda backend to handle requests from the React frontend

def lambda_handler(event, context):
    if event['path'] == '/api/forecast':
        # Call forecast function
        emissions_forecast = forecast_emissions()
        return {
            'statusCode': 200,
            'body': json.dumps(emissions_forecast.tolist())
        }
    
    if event['path'] == '/api/optimal-usage':
        # Optimize based on forecast
        baseline_emissions = 500  # Placeholder
        emissions_forecast = np.random.rand(336)  # Placeholder data
        optimal_usage = optimize_energy_usage(emissions_forecast, baseline_emissions)
        return {
            'statusCode': 200,
            'body': json.dumps(optimal_usage.tolist())
        }

    return {
        'statusCode': 404,
        'body': json.dumps('Endpoint not found')
    }
