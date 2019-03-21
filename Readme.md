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
docker-compose exec stocktrend python3 stocktrend.py
```

## Test
* Test with curl
```
curl --header "Content-Type: application/json" --request POST --data '{"symbol":"MSFT","trenddays":3}' http://127.0.0.1:8511/trendclose
```
Output should be similar to: `{"lastclose": 117.52, "trend": -0.04}`