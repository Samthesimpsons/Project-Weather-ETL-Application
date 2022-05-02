import boto3
import pandas as pd
import os
import requests
import io

# Environment variables
S3_BUCKET = os.environ['S3Bucket']
LOCATION_LAT = os.environ['Lat']
LOCATION_LONG = os.environ['Long']

# Lambda function handler
def lambda_handler(event, context):
    
    LAT = str(LOCATION_LAT)
    LONG = str(LOCATION_LONG)

    # "Daily" parameter results in nested json results of the current + 7 days forecasted weather
    fetched = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+LAT+"&lon="+LONG+"&exclude=current,minutely,alerts,hourly&appid=4e85512db10f65ee2dc95e2c616694ac")
    json_obj = fetched.json()

    # Get the current datetime of the API Query
    current_dt = json_obj['daily'][0]['dt']

    # Place json results in a tidy pandas table
    df_flat = pd.json_normalize(json_obj['daily'])
    df_flat['Lat'], df_flat['long'], df_flat['timezone'],  df_flat['timezone_offset'] = list(pd.json_normalize(json_obj).values[0][0:4])

    # Calculate the average weekly forecasted maximum temp and append to the table
    sum_forecasted_maxtemp = 0
    for i in range(1,len(json_obj['daily'])):
        sum_forecasted_maxtemp += json_obj['daily'][i]['temp']['max']
    df_flat['Max_weekly_temp'] = sum_forecasted_maxtemp/len(json_obj['daily'])

    # File name for csv
    FILENAME = str(current_dt)

    # Save files into S3
    url = 's3://{}/{}'.format(S3_BUCKET, FILENAME)
    df_flat.to_csv(url)