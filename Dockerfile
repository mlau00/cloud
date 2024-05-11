# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /python-docker

# Set Flask environment variable; it changes .env file :)
ENV FLASK_ENV=production

RUN apt-get update && apt-get -y install libpq-dev gcc 
# wget

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#
# RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
# RUN chmod +x cloud_sql_proxy
#
COPY . .

# Expose the port your application will run on
EXPOSE 8080

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# Define the command to run the Flask app
# CMD ["./cloud-sql-proxy universityprojectml:europe-west1:postgresql-instance", "python", "app.py"]
CMD ["python", "app.py"]
