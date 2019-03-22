import os
from flask import Flask, request
from stocktrend import getstockjson, getstockclosingprice, getstocktrend, getjsonreturn

app = Flask(__name__)

@app.route("/trendclose", methods=['POST'])
def trendclose():
    if request.method == 'POST':
        symbol = request.json['symbol']
        trenddays = request.json['trenddays']
        jsondata = getstockjson(os.environ["APIKEY"], symbol)
        closing = getstockclosingprice(jsondata, 1)
        trend = getstocktrend(jsondata, trenddays)
        return getjsonreturn(closing, trend)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ["PORT"])