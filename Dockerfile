FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG PORT=5000
ENV PORT=$PORT
EXPOSE $PORT

VOLUME /app/translated_files

ENTRYPOINT ["python3", "translation_api.py"]
