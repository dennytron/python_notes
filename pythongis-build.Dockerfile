FROM osgeo/gdal:ubuntu-full-3.2.2

RUN apt-get update
RUN apt-get install software-properties-common -y

# for psycopg2 from source
#RUN apt-get install libpq-dev gcc -y

# install Python
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update -y
RUN apt-get install python3.9 -y

# depending on what packages you need...
RUN apt-get install python3.9-dev -y

# install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt-get install python3-distutils -y
RUN python3.9 get-pip.py

COPY requirements.txt /app/requirements.txt
RUN pip3.9 install -r /app/requirements.txt
COPY . /app

WORKDIR /app
