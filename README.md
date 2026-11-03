## Quick start

1. Clone the repository:

       git clone https://github.com/winnieswl/coding-test.git
       cd coding-test

2. Add the data. Copy the files provided by Treefera into a `data/` folder at the project root:

       data/
           fr_de_wheat_cube.zarr/
           geometry.parquet

3. Run in Docker:

       docker build -t treefera-coding-test:v1 .
       docker run --rm \
         -v "$PWD/data":/data:ro \
         -v "$PWD/output":/output \
         -e DATA_DIR=/data -e OUTPUT_DIR=/output \
         treefera-coding-test:v1 --crop <crop> --season <season> --as-of <as-of-date>

   Or run locally with uv (Python 3.13):

       uv sync
       DATA_DIR=data OUTPUT_DIR=output uv run treefera-coding-test --crop <crop> --season <season> --as-of <as-of-date>

    * `<crop>` is optional. Default is "fr_de_wheat", which represents wheat in France and Germany
    * `<season>` is optional. Default is 2024.
    * `<as-of-date>` is required, in format of YYYY-MM-DD.

Predictions are written to `output/`.

