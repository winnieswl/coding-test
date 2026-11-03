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

    * <crop> is optional. Default is "fr_de_wheat", which represents wheat in France and Germany
    * <season> is optional. Default is 2024.
    * <as-of-date> is required, in format of YYYY-MM-DD.

Predictions are written to `output/`.

## Answers to tasks

around 30 minutes loading data and reviewing data
around 60 minutes to design and test v1
around 30 minutes to containerise and test 

1. Define v1 model: define the simplest model you can imagine (even just a random number generator). We are not interested in your modelling decisions here, more the deployment, promotion and observation of models in production.

    * Approach: 
        * Forecast is assumed to be the regional average yield calculated from the 5 most recent year based on as-of date. (e.g. For as-of date of 2022-06-01, it will use 2018-2022 data.)
    * Possible limitations:
        * Some regions may have incomplete yield data, so 5-year average might contain less than 5 values. 
        * If yield is not available for the as-of date, the forecast will be a 4-year average. 
        * This approach only depend on the "as_of_date", so ideally the "as_of_date" should be closer to the "forecast_data". Using older as_of_date may not be sensible approach. (e.g. Using the 5-year average between 2005-2009 to forecast yield in 2025).
        * The current v1 model code only compute yield for a single crop type.

2. Deploy v1 model. Package the baseline so it can run as a batch prediction job: given a crop, a season and an as-of date, it produces regional yield estimates. It should build and run from a clean clone, with versioned artefacts and no data or secrets baked into the image. Tell us how you would schedule it. We use dagster internally.

    * Containerised v1 model in Docker image. Takes crop, season and as-of date as input, though the variable "season" is not used in v1 of model.
    * Scheduling:
        * Trigger run when latest yield data is available since v1 model only uses historic yield data.
        * If newer version is introduced and is run at a more frequent schedule, I would run v1 model more frequently to match the newer version to allow comparison. 

3. Promote or not. Build a v2 you believe improves on v1, then decide whether it should replace v1 in production, it can be as simple as an interaction effect. Set out the evidence and the criteria you used, and what you would do before switching over. This is very similar to our promotion process internally.

    * For v2, take into account of latest rainfall and temperature. 
    * Criteria for promotion:
        * Improvement in RMSE: RMSE from v2 is at least 5% less than v1
        * Compare RMSE for v1 and v2 across 10 years: v2's RMSE is lower than v1's RMSE for at least 6 years
        * For now, the "weights" of rainfall and temperature will be fixed. If they were calibrated from historic data, also need to consider the stability of the calibrated parameters. E.g. "weightings" calibrated from each set of historic data remain within +/- 5%. The calibrated parameters should also be sensible. 
    * Steps before switching over:
        * Run both versions in production for a duration of time (e.g. 2 months) to observe how v1 and v2 perform. The performance may include: forecast output, runtime, error messages. During the "test" run period, users may not see the output from v2 model until fully tested. 
        * Once confidence on v2 model is established, may roll out this version to a subset of users to introduce this version in phases.
        * When rolling out new version, we should also communicate with user what changes the new version include, and how they should expect the performance to change. The change in performance could cover: runtime, accuracy, uncertainty/confidence of output.  

4. Observe. Write a short design for monitoring this model in live use. We want to see how you would visualise the model as it runs each week - what inputs have changed, how has that impacted the output predictions and data drift checks. Bear in mind that actual yields arrive a year late: tell us what you would watch in the meantime, what would trigger an alert, and how you would evaluate the model once yields are published. This task is a written design; you do not need to build it.

