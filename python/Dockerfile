FROM python:3.6.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk --no-cache add gcc musl-dev g++

RUN pip install -qr requirements.txt && rm -rf requirements.txt

COPY main.py .

RUN addgroup -S app && adduser -S app -G app && \
    chown -R app /app

USER app

EXPOSE 8000

CMD ["python", "main.py"]