FROM ubuntu:18.04

RUN apt-get update && apt-get install -qy python \ python-pip
RUN apt install python3-pip
RUN pip3 install beautifulsoup4

COPY entrypoint.sh /entrypoint.sh
COPY extractReport.py /usr/bin/extractReport.py

ENTRYPOINT ["/entrypoint.sh"]