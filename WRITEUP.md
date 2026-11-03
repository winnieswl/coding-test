## Task 1 Define v1 model:
define the simplest model you can imagine (even just a random number generator). We are not interested in your modelling decisions here, more the deployment, promotion and observation of models in production.

    * Approach: 
        * Forecast is assumed to be the regional average yield calculated from the 5 most recent year based on as-of date. (e.g. For as-of date of 2022-06-01, it will use 2018-2022 data.)

    * Possible limitations:
        * Some regions may have incomplete yield data, so 5-year average might contain less than 5 values. 
        * If yield is not available for the as-of date, the forecast will be a 4-year average. 
        * This approach only depend on the "as_of_date", so ideally the "as_of_date" should be closer to the "forecast_data". Using older as_of_date may not be sensible approach. (e.g. Using the 5-year average between 2005-2009 to forecast yield in 2025).
        * The current v1 model code only compute yield for a single crop type.

## Task 2 Deploy v1 model. 
Package the baseline so it can run as a batch prediction job: given a crop, a season and an as-of date, it produces regional yield estimates. It should build and run from a clean clone, with versioned artefacts and no data or secrets baked into the image. Tell us how you would schedule it. We use dagster internally.

    * Containerised v1 model in Docker image. Takes crop, season and as-of date as input, though the variable "season" is not used in v1 of model.
    * Scheduling:
        * Trigger run when latest yield data is available since v1 model only uses historic yield data.
        * If newer version is introduced and is run at a more frequent schedule, I would run v1 model more frequently to match the newer version to allow comparison. 

## Task 3 Promote or not. 
Build a v2 you believe improves on v1, then decide whether it should replace v1 in production, it can be as simple as an interaction effect. Set out the evidence and the criteria you used, and what you would do before switching over. This is very similar to our promotion process internally.

    * For v2, take into account of total rainfall in most recent winter of forecast year. 
    * Criteria for promotion:
        * Improvement in RMSE: RMSE from v2 is at least 5% less than v1
        * Compare RMSE for v1 and v2 across 10 years: v2's RMSE is lower than v1's RMSE for at least 6 years
        * For now, the "weights" of rainfall will be fixed. If they were calibrated from historic data, also need to consider the stability of the calibrated parameters. E.g. "weightings" calibrated from each set of historic data remain within +/- 5%. The calibrated parameters should also be sensible. 
    * Steps before switching over:
        * Run both versions in production for a duration of time (e.g. 2 months) to observe how v1 and v2 perform. The performance may include: forecast output, runtime, error messages. During the "test" run period, users may not see the output from v2 model until fully tested. 
        * Once confidence on v2 model is established, may roll out this version to a subset of users to introduce this version in phases.
        * When rolling out new version, we should also communicate with user what changes the new version include, and how they should expect the performance to change. The change in performance could cover: runtime, accuracy, uncertainty/confidence of output.  
    * Promotion decision:
        * Not decided yet, as will need to test and compare the approaches.
        * I would back-test v1 and v2 using older datset, then evaluate the models based on my criteria for promotion above. 

## Task 4 Observe. 
Write a short design for monitoring this model in live use. We want to see how you would visualise the model as it runs each week - what inputs have changed, how has that impacted the output predictions and data drift checks. Bear in mind that actual yields arrive a year late: tell us what you would watch in the meantime, what would trigger an alert, and how you would evaluate the model once yields are published. This task is a written design; you do not need to build it.

    * Monitoring model:
        * Data input:
            * Monitor new data inputs for anomalies. E.g. Regional total rainfall in months remain within +/- 5%.
            * Monitor distributions for new data inputs align with calibration data. 
            * Monitor portion of missing data. New data should not contain significantly more missing data
        * Data output:
            * Monitor output are within +/- 5% of regional mean. 
            * Monitor shifts in output is consistent with shifts in input data. E.g. expect lower yield if this year seems excessive winter rainfall.
        * Model performance:
            * Monitor model run time, significantly shorter runtime could be caused by input data issues. 
        * Model parameters:
            * If model depends on calibrated parameters that are updated regularly, monitor the calibrated parameters remain within +/- 5%. More significant changes may require additional investigation.
            * If model depends on static parameters, we will also need to monitor or assess if static parameters are still valid with new climate data. 
        * Delay in yield data:
            * Monitor input climate data, to check that the latest climate metrics are within our historical range. If climate data shows abnormal value, we may expect yield for this year to be outside of expected range. (E.g. year of extremely dry summer and wet winter) This may trigger an alert to evaluate the model by comparing it to other "extreme" years in the past. 
            * Also may need to consider increase of extreme weather events intensity and frequency, whose impact on crop yield may not be fully captured by climate data used in the model. 
        * Model evaluation:
            * Once new data is published, I would compare model forecast against the latest data, to assess whether current approach is still valid by evaluating the RMSE, but a larger RMSE may also be related to "abnormal" weather conditions for that particular year, so a large RMSE may not necessarily mean the model is no longer valid. 
        * Visualisation:
            * Since we're interested in monitoring live use, I would display a map of the region of interest, colouring by the difference between current forecast and the average yield among recent years.
            * I would also include a similar map, coloured by the difference between most recent climate / soil data (e.g. total rainfall) and the average climate / soil data. This would help understanding whether any shifts in output is expected from any shift in input. 