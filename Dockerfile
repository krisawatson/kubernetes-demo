FROM alpine:3.7

COPY requirements.txt /tmp/requirements.txt
RUN apk add --update python python-dev py-pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt
RUN mkdir /tmp/data

ADD src /etc/demo
WORKDIR /etc/demo

EXPOSE 8237

CMD [ "python", "app.py" ]
