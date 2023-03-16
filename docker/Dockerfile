FROM python:3.9-slim-buster

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

ARG BOXID
ARG NODEIP
ENV boxid=${BOXIDID}
ENV nodeip=${NODEIP}
COPY box.py /

ENTRYPOINT ["python", "/box.py"]
CMD []
