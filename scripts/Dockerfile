FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add --no-cache curl tcpdump
RUN apk add bash
RUN pip install mysql-connector-python
COPY . .
CMD ["python", "./app.py"]
