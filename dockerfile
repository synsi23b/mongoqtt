FROM python:latest

WORKDIR /src

ADD requirements.txt /src/
RUN pip3 install -r requirements.txt
ADD ./* /src/
CMD ["python3", "server.py"]