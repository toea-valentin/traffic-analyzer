FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install prometheus-client mysql-connector-python
EXPOSE 8000
COPY . .
CMD ["python", "./exporter.py"]