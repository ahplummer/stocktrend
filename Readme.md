# Instructions

## Build/Run container
* Set / Inject environment variables:
```
export STOCKTREND_PORT=8511
export STOCKTREND_APIKEY=<get your key at https://www.alphavantage.co>
```
* Build docker image:
```
docker-compose up -d --build
```
* Run docker image via docker-compose:
```
docker-compose exec stocktrend python3 driver.py
```

## Test
* Test with curl
```
curl --header "Content-Type: application/json" --request POST --data '{"symbol":"MSFT","trenddays":3}' http://127.0.0.1:8511/trendclose
```
Output should be similar to: `{"lastclose": 117.52, "trend": -0.04}`

# Build/Run Serverless (AWS Lambda)
Look at the `handler.py` file for more information, as there are some lessons learned through building 
this that are significant.
## Test
* Deploy with sls CLI:
```
sls deploy
```
NOTE: copy down the output URL for later testing via `curl`.
```
Service Information
service: stocktrend
stage: dev
region: us-east-1
stack: stocktrend-dev
resources: 10
api keys:
  None
endpoints:
  POST - https://kwbp75f9p0.execute-api.us-east-1.amazonaws.com/dev/trendclose
functions:
  trendclose: stocktrend-dev-trendclose
layers:
  None
```
* Test with sls CLI:
```
sls invoke -f trendclose -l -d '{"apikey":"P7HHSPMQIGVSI3Q8","symbol":"AAL","trenddays":3}'
```
This is what the output shows (with extra logging):
```
{
    "statusCode": 200,
    "body": "{\"lastclose\": 30.96, \"trend\": -1.34}"
}
--------------------------------------------------------------------
START RequestId: 4f1ec5ef-b74f-46cd-8b46-53716102e665 Version: $LATEST
Fetching https://www.alphavantage.co/query?apikey=P7HHSPMQIGVSI3Q8&function=TIME_SERIES_DAILY_ADJUSTED&symbol=AAL
END RequestId: 4f1ec5ef-b74f-46cd-8b46-53716102e665
REPORT RequestId: 4f1ec5ef-b74f-46cd-8b46-53716102e665	Duration: 227.07 ms	Billed Duration: 300 ms 	Memory Size: 1024 MB	Max Memory Used: 67 MB
```
* Test with curl:
```
curl --header "Content-Type: application/json" --request POST --data '{"apikey":"P7HHSPMQIGVSI3Q8","symbol":"AAL","trenddays":3}' https://kwbp75f9p0.execute-api.us-east-1.amazonaws.com/dev/trendclose
```
This is what the output shows: `{"lastclose": 30.96, "trend": -1.34}%`

## Remove from Lambda
```
sls remove
```