# set base image (host OS)
FROM python:3.8-alpine

# set labels
LABEL maintainer="Tóth Krisztián Gyula <ktothdev@gmail.com>" \
      version="1.0.0"

# pip is upgraded before using a worker user, because it’s installed as root and can’t be accessed by a non-root user
RUN pip install --upgrade pip

# create a non-root user
RUN adduser -D worker
USER worker

# set the working directory in the container
WORKDIR /home/worker/app

# copy the dependencies file to the working directory
COPY --chown=worker:worker requirements.txt requirements.txt
# installs the dependencies for the current user in the .local/bin directory
RUN pip install --user -r requirements.txt
# we need to add this newly created directory to the PATH environment variable
ENV PATH="/home/worker/.local/bin:${PATH}"

# copy the content of the local src directory to the working directory
COPY --chown=worker:worker src/app .

EXPOSE 5000
ENV FLASK_APP=/home/worker/app/app.py

ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]