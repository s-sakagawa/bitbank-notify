FROM python:3.8-alpine

ENV WORKSPACE /var/www/

WORKDIR $WORKSPACE

RUN apk update && \
    apk add bash && \
    apk add git

RUN pip install requests && \
    pip install git+https://github.com/bitbankinc/python-bitbankcc.git

COPY main.py $WORKSPACE
COPY ./src/ $WORKSPACE/src

CMD ["python"]
