# Design Documentation

## Initial Project Background

A data science team is building a data application for fleet management, and they feel that weather data will be useful. They want a data pipeline to extract, transform and load the weather data into the data lake, so that they can analyze this data.

- Create a data pipeline;
- Load weather data from a public weather API;
- Calculate the maximum weekly temperature when it is raining;
- Store the data in a data storage.

## Assumptions

The assumption is that daily weather forecast is needed for analysis by the data science team. In order to use this data for fleet management, they will require forecasted data too. As such if the current day weather is rainy, they would hypothetically want to understand the weather in the following 7 days and calculate the maximum weekly temperature.

# System Architecture

Since we are going to be dealing with small data feeds of (current + 7 day forecast) daily, we do not require complex and expensive computational resources. 

Therefore I am going to go with an Micro ETL data pipeline using AWS services:

Stack deployed using `AWS SAM CLI`:
- A daily (time-based) triggers an `AWS Lambda` function that 
    * Extracts data from the `Open Weather One Call API`
    * Transforms the heavily nested raw data from the API into a neat tidy pandas dataframe clean format
    * Calculate the forecasted maximum average weekly temperature
- Transformed cleaned content will be stored in an `Amazon Simple Storage S3` bucket as CSV files. 

The user can head over to the `AWS Lambda` to change the environment variables which includes the `Lat` and `Long` coordinates.

# Maintenance Documentation

# Setup Documentation

## Working Directory

First, change the working directory into  `Carro_Assigment` after cloning from the Github repository.

## Setting Up Environment

First, we shall use a conda environment to run everything which will handle all the dependencies and install python for us.

1. Open up the `Anaconda Prompt` shell, then first let us create our conda environment:

    ```console
    conda env create -f environment.yml
    ```

2. Activate our conda environment using:

    ```console
    conda activate weather-micro-etl
    ```

## AWS SAM Application:

The entire AWS SAM application is under the `weather-etl-app` directory.

There are **three** components

1. `template.yml`
    - Contains the configuration to build and the schedule to deploy the Lambda function daily;
2. `application/app.py` 
    - Contains the code of our application;
    - AWS Lambda handler function contains the API query, transformation step, maximum temperature calculation, and saves the results to a CSV file into our S3 Bucket.
3. `application/requirements.txt`
    - Contains a list of Python libraries needed for our function to run

## Deployment of ETL

Now to build and deploy the application using the AWS SAM CLI:

1. Change the working directory into the `weather-etl-app` folder;
2. Run the build command to let AWS SAM compile and bundle our application together with the dependencies;

    ```console
    sam build
    ```
3. Deploy the ETL process to AWS, stack name shall just be `weather-micro-etl` and follow the default for all the guided prompts (ensure the region is `us-east-1` due to location constraints);

    ```console
    sam deploy --guided
    ```
4. Testing by simply invoking the function by testing it on the `AWS Lambda` console and then moving to the `S3 Bucket` console to check for the file. If there is a permission error, check the permissions for the IAM role for the ETL function and ensure `AmazonS3FullAccess` permission policy has been added.
At the very end, to delete the stack, we can delete the stack on the AWS CloudFormation console.

5. The user can now simply download the file from the S3 Console or run an S3 SQL Query. Since the Query is not complex, we do not need to integrate with `Amazon Athena`. An example of a daily result is shown in `results.csv`

    ```console
    SELECT * FROM s3object s 
    ```