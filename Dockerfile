FROM python:3.10.5

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY . /src
# Install dependencies
RUN apt-get update && apt-get install make
RUN pip install -r requirements.txt

RUN make generate-listings-outcode-csv-file



# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /src

RUN make generate-listings-outcode-csv-file

RUN ls .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
