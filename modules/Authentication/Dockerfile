# our base image
FROM python:3.8-alpine

# Install python and pip
#RUN apk add --update py2-pip

RUN pip install --upgrade pip

WORKDIR /app
COPY . .

# install Python modules needed by the Python app
RUN pip install --no-cache-dir -r requirements.txt

# copy files required for the app to run
# tell the port number the container should expose
EXPOSE 5002

# run the application
ENV FLASK_APP=app.py
# run the application
#CMD python app.py

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5002"]
