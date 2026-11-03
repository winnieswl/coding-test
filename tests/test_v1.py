import xarray as xr 
import pytest
import pandas as pd
import numpy as np
from treefera_coding_test.models.v1 import compute_moving_mean

@pytest.fixture
def sample_yield():
    regions = ["FR01", "FR10", "DE11"]
    years = [2017, 2018, 2019, 2020, 2021, 2022]
    
    return xr.DataArray(
        [
            (10.0, 15.0, 20.0, 25.0, 30.0, 35.0),
            (np.nan, 15.0, 20.0, np.nan, 40.0, 35.0),
            (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan),
        ],
        dims=("adm_id", "year"),
        coords={"adm_id": regions, "year": years},
    )

def test_compute_moving_mean(sample_yield):
    res = compute_moving_mean(sample_yield, 2021, window=5)
    print(res)
    base_res = xr.DataArray(
        [
            20.0,
            25.0,
            np.nan,
        ],
        dims="adm_id",
        coords={
            "adm_id": ["FR01", "FR10", "DE11"]
        },
    )
    xr.testing.assert_allclose(res, base_res)

    return