import os, json
from stocktrend import getstockjson, getstockclosingprice, getstocktrend, getjsonreturn

def trendclose_handler(event, context):
    #NOTE: the event parsing was difficult to debug when fronted by the gateway.
    #see https://forums.aws.amazon.com/thread.jspa?messageID=869755&tstart=0
    #the `sls invoke ...` command worked perfectly, while curl didn't.
    #the postman/curl commands went through the gateway, which wrapped data around the body
    try:
        symbol = event['symbol']
        trenddays = event['trenddays']
        apikey = event['apikey']
    except:
        # Gets data that gets wrapped up from API Gateway
        postdata = json.loads(event['body'])
        symbol = postdata['symbol']
        trenddays = postdata['trenddays']
        apikey = postdata['apikey']
    jsondata = getstockjson(apikey, symbol)
    closing = getstockclosingprice(jsondata, 1)
    trend = getstocktrend(jsondata, trenddays)
    body = getjsonreturn(closing, trend)

    #see https://aws.amazon.com/premiumsupport/knowledge-center/malformed-502-api-gateway/
    #had issue with results, as they have to match this format, otherwise 502's occur
    #when invoked from `curl`. `sls invoke ...` worked fine
    results = {
        #"isBase64Encoded": true|false,
        #"headers": { "headerName": "headerValue", ... },
        "statusCode": 200,
        "body": body
    }
    return results

if __name__ == "__main__":
    #really for testing this driver out locally.
    eventdic = { "apikey": os.environ['APIKEY'],
                 "symbol": "MSFT",
                 "trenddays": 3}
    results = trendclose_handler(eventdic,'')
    print(results)