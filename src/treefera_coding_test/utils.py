import xarray as xr

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