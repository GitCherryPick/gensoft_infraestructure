FROM python:3.9-slim

RUN adduser --disabled-password --gecos '' sandboxuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-asyncio
COPY . /app

RUN chown -R sandboxuser:sandboxuser /app

USER sandboxuser

EXPOSE 8002

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002" ]