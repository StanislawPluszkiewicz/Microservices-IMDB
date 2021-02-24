# our base image
FROM python:3.8-alpine

# Install python and pip
#RUN apk add --update py2-pip

RUN pip install --upgrade pip

WORKDIR /app
COPY . .

RUN apk add --update --no-cache --virtual .build-deps g++ gcc libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir lxml>=3.5.0 && \
    apk del .build-deps

# works too, is faster but takes more space
#RUN apk add --update --no-cache g++ gcc libxslt-dev
    
# install Python modules needed by the Python app
RUN pip install --no-cache-dir -r requirements.txt

# copy files required for the app to run
# tell the port number the container should expose
EXPOSE 5013

ENV FLASK_APP=app.py
# run the application
#CMD python app.py

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5013"]
