import urllib.request, json

def getstockclosingprice(jsondata, day):
    if (day is None) or (day <= 0):
        return 'Bad parameter for day....'
    dayswalked = 0 #skip today
    for key in jsondata["Time Series (Daily)"]:
        if dayswalked == day:
            result = jsondata["Time Series (Daily)"][key]["4. close"]
            break
        dayswalked += 1
    result = float(result)
    return result

def getstocktrend(jsondata, days):
    if (days is None) or (days <= 0):
        return 'Bad parameter for days....'
    closings = []
    for i in range(1, days+1):
        closings.append(getstockclosingprice(jsondata, i))
    firstday = closings[len(closings)-1]
    lastday = closings[0]
    if firstday > lastday: #find decrease percentage
        result = ((firstday - lastday) / firstday) * 100 * -1
    else: #find increase percentage
        result = ((lastday - firstday) / firstday) * 100
    return round(result, 2)

def getstockjson(apikey, symbol):
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    baseurl = 'https://www.alphavantage.co/query'
    fullurl = baseurl + '?apikey=' + apikey + '&function=' + \
                   function + '&symbol=' + symbol
    print('Fetching ' + fullurl)
    with urllib.request.urlopen(fullurl) as response:
        result = json.loads(response.read().decode())
    return result

def getjsonreturn(closing, trend):
    result = { "lastclose": closing, "trend": trend}
    result = json.dumps(result)
    return result
