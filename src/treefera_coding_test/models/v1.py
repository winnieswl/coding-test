import xarray as xr
import pandas as pd

from treefera_coding_test.data import load_crop_data
from treefera_coding_test.utils import compute_moving_mean

def v1(crop: str, season: int, as_of_date: pd.Timestamp) -> xr.Dataset:

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

    # Convert string as_of_date to int as_of_year
    as_of_year = as_of_date.year   
    # Return 5-year average yield at regional level
    regional_mean = compute_moving_mean(crop_data["yield"], as_of_year, window=5)
    
    # TODO: Check size of output matches input
    # TODO: Add checks to values outside of expected range (e.g., negative values, extremely high values)

    return regional_mean