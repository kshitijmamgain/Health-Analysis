# Use an official Node runtime as the parent image
FROM python:3.8.5

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
EXPOSE 8080
CMD python ./app.py