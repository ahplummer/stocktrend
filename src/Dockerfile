FROM alpine:3.9

ADD ./*.* /stocktrend/

RUN apk add --no-cache python3 python3-dev bash build-base

RUN cd /stocktrend && pip3 install -r requirements.txt

WORKDIR /stocktrend
