""" Data processing functions for handling crop data. """

import xarray as xr


def load_crop_data(crop: str) -> xr.Dataset:
    """
    Load crop data from a Zarr file based on the specified crop type.

    Parameters:
    crop (str): The type of crop (e.g., 'soft wheat').

    Returns:
    xr.Dataset: The loaded xarray Dataset containing the crop data.
    """
    # Load the crop data from the corresponding Zarr file
    crop_data = xr.open_zarr(f"data/{crop}_cube.zarr")

    # For v1, we need "year", "adm_id", and "yield" variables. Ensure these are present in the dataset.
    if "yield" not in crop_data.data_vars:
        raise ValueError("Yield variable missing from crop data")
    if "year" not in crop_data.coords:
        raise ValueError("Year coordinate missing from crop data")
    if "adm_id" not in crop_data.coords:
        raise ValueError("Adm_id coordinate missing from crop data")
    # TODO: Add checks for input data quality, e.g. portion of missing values, range of yield data, etc.
    
    return crop_data