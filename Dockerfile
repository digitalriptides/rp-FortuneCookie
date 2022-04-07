#Starting with python base image
FROM python:3.8-slim  


# add user (change to whatever you want)
# prevents running sudo commands
RUN useradd -r -s /bin/bash cookieuser

# set current env
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

RUN chown -R cookieuser:cookieuser /app
USER cookieuser

# set app config option
ENV FLASK_ENV=production

# set argument vars in docker-run command
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION


ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# Avoid cache purge by adding requirements first
ADD ./requirements.txt ./requirements.txt

# Installing the requirements
RUN pip install --no-cache-dir -r ./requirements.txt --user

# Add the rest of the application files
COPY . /app
WORKDIR /app

# Run and start web server GUnicorn, using port 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]