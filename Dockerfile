FROM python:3-slim

# Install Requirements
RUN apt-get update -y && apt-get install -y python3-pip python3-wheel
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt

# Copy Application into Image/Container
COPY . /app
EXPOSE 5000:5000
ENTRYPOINT ["python"]
CMD [ "-u", "main.py"]
