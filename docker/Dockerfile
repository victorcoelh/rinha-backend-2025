FROM python:3.13-slim-trixie
WORKDIR /api
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN export PYTHONPATH="${PYTHONPATH}:/api/"
RUN pip install -r requirements.txt
#RUN python -m compileall -q ./src/
