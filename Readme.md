# Instructions

## Setup environment
*Note: all commands executed from top-level project directory, unless specified differently.*
* Setup a virtualenv: `virtualenv --python=python3 .venv`
* Startup the virtualenv: `. .venv/bin/activate`
* Get requirements: `pip install -r src/requirements.txt`
* Get an API key [here](https://www.alphavantage.co).
### Run tests
* To run unit tests: `pushd test && python -m unittest && popd`

## Run locally
* Set environment variables:
```
export PORT=8511
export APIKEY=<your key>
```
* Start Flask Webserver locally with `python src/driver.py`.

### Test local endpoint
* Use with curl from a new terminal:
```
curl --header "Content-Type: application/json" --request POST --data '{"symbol":"AAL","trenddays":3}' http://127.0.0.1:8511/trendclose
```
Output should be similar to: `{"lastclose": 31.45, "trend": -0.44}%`

## Build/Run container
* Set / Inject environment variables:
```
export STOCKTREND_PORT=8511
export STOCKTREND_APIKEY=<your key>
```
* Build docker image:
```
docker-compose up -d --build
```
* Run docker image via docker-compose:
```
docker-compose exec stocktrend python3 driver.py
```

### Test dockerized endpoint
* Use with curl from a new terminal:
```
curl --header "Content-Type: application/json" --request POST --data '{"symbol":"AAL","trenddays":3}' http://127.0.0.1:8511/trendclose
```
Output should be similar to: `{"lastclose": 31.45, "trend": -0.44}%`


## Build/Run Serverless (AWS Lambda)
*Prerequisite: You must have `serverless` installed. See [Serverless.com](http://serverless.com) for more information.*
*Prerequisite: You must have `AWS CLI` installed, and have it configured to execute from the command line. You can test 
this with `aws s3 ls`. If you get no errors, you can proceed.

NOTE: Look at the `handler.py` file for more information, as there are some lessons learned through building 
this that are significant.

### Build Lambda
* Deploy with sls CLI:
```
pushd src && sls deploy && popd
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
  POST - https://9eip1rau0j.execute-api.us-east-1.amazonaws.com/dev/trendclose
functions:
  trendclose: stocktrend-dev-trendclose
layers:
  None
```
### Test serverless Lambda endpoint:

* Test with sls CLI:
```
pushd src && sls invoke -f trendclose -l -d '{"apikey":"<your key>","symbol":"AAL","trenddays":3}' && popd
```
This is what the output shows (with extra logging):
```
{
    "statusCode": 200,
    "body": "{\"lastclose\": 31.45, \"trend\": -0.44}"
}
```
* Test with curl from another terminal:
```
curl --header "Content-Type: application/json" --request POST --data '{"apikey":"$APIKEY","symbol":"AAL","trenddays":3}'  https://9eip1rau0j.execute-api.us-east-1.amazonaws.com/dev/trendclose
```
This is what the output shows: `{"lastclose": 31.45, "trend": -0.44}%`

### Remove from Lambda
```
pushd src && sls remove && popd
```
### Clean up 
```rm -rf src/.serverless```