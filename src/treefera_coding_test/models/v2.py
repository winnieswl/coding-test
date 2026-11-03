import xarray as xr
import pandas as pd

from treefera_coding_test import data
from treefera_coding_test.data import load_crop_data
from treefera_coding_test.utils import compute_moving_mean, compute_anomalies

def v2(crop: str, season: int, as_of_date: pd.Timestamp) -> xr.Dataset:

    """
    Main function to load and process crop data based on the specified crop, season, and as_of_date.

    Parameters:
    crop (str): The type of crop (e.g., 'soft wheat').
    season (int): The year of season for which to load the data (e.g., 2024, 2025). This parameter is not used in this version. 
    as_of_date (str): The date up to which the data should be considered (format: 'YYYY-MM-DD').

    Returns:
    xr.Dataset: The processed xarray Dataset containing the relevant crop data.
    """

    # Load the crop data based on the specified parameters
    crop_data = load_crop_data(crop)

    # Load the model parameters for the specified crop and season
    # TODO: Calibrate model parameters, for now, uses dummy values
    params = {"rainfall": -0.2}

    # Convert string as_of_date to int as_of_year
    as_of_year = as_of_date.year   

    # Return 5-year average yield and rainfall at regional level
    yield_mean = compute_moving_mean(crop_data["yield"], as_of_year, window=5)

    # Compute winter rainfall anomalies based on the as_of date
    rainfall_anomaly = compute_anomalies(crop_data["prec"], as_of_year, season, 5) 

    # v2 introduces adjustments based on rainfall and temperature anomalies.
    forecast = yield_mean + params["rainfall"] * rainfall_anomaly
    
    return forecast