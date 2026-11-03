import xarray as xr
import pandas as pd

def compute_moving_mean(data: xr.DataArray, as_of_year: int, window: int) -> xr.DataArray:
    """
    Compute the moving mean of the given data over a specified window.

    Parameters:
    data (xr.DataArray): The input data array.
    as_of_year (int): The year up to which the data should be considered.
    window (int): The size of the moving window.

    Returns:
    xr.DataArray: The data array with the moving mean computed.
    """
    # Implementation for computing moving mean
    # TODO: Handle regions where all years in the window are missing (e.g., return NaN for those regions)
    # TODO: Also consider alternative handling for partially missing data within the window
    return data.sel(year=slice(as_of_year-window+1, as_of_year)).mean(dim="year")

def compute_anomalies(data: xr.DataArray, as_of_year: pd.Timestamp, forecast_year: int, window: int) -> xr.DataArray:
    """
    Compute the anomalies of the given data based on the as_of_year and forecast_year.

    Parameters:
    data (xr.DataArray): The input data array.
    as_of_date (pd.Timestamp): The date up to which the data should be considered.
    forecast_year (int): The year for which the forecast is being made.
    window (int): The size of the moving window.

    Returns:
    xr.DataArray: The data array with anomalies computed.
    """
    current_winter = forecast_year - 1                      # Oct–Dec before harvest
    normal_years = range(as_of_year - window, current_winter)

    def winter_total(y):
        return data.sel(date=slice(f"{y}-10-01", f"{y}-12-31")).sum(dim="date")

    normal = xr.concat([winter_total(y) for y in normal_years], dim="year").mean(dim="year")

    latest = winter_total(current_winter)
    return ((latest - normal) / normal)


    
