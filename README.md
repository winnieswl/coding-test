
around 30 minutes loading data and reviewing data

Define v1 model: define the simplest model you can imagine (even just a random number generator). We are not interested in your modelling decisions here, more the deployment, promotion and observation of models in production.

* let do 5-year average yield at regional level
* possible limitations: some regions may have incomplete yield data, so 5-year average might contain less than 5 values. if as_of_date is further back (e.g. 2009), using the 5-year average to forecast e.g 2020 yield may lead to large error.


Deploy v1 model. Package the baseline so it can run as a batch prediction job: given a crop, a season and an as-of date, it produces regional yield estimates. It should build and run from a clean clone, with versioned artefacts and no data or secrets baked into the image. Tell us how you would schedule it. We use dagster internally.



Promote or not. Build a v2 you believe improves on v1, then decide whether it should replace v1 in production, it can be as simple as an interaction effect. Set out the evidence and the criteria you used, and what you would do before switching over. This is very similar to our promotion process internally.



Observe. Write a short design for monitoring this model in live use. We want to see how you would visualise the model as it runs each week - what inputs have changed, how has that impacted the output predictions and data drift checks. Bear in mind that actual yields arrive a year late: tell us what you would watch in the meantime, what would trigger an alert, and how you would evaluate the model once yields are published. This task is a written design; you do not need to build it.

