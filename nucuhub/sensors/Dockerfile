# To build this image use the following command:
# docker build ./nucuhub -f ./nucuhub/sensors/Dockerfile -t nucuhub.sensors
# To debug: docker run -it nucuhub.sensors /bin/bash
FROM ubuntu:bionic
MAINTAINER Denis Nutiu

WORKDIR app

# Copy the NucuHub folder into the workdir
COPY . .

# Share the volumes; Used to access GPIO ports.
VOLUME ["/sys/class/thermal/", "/sys/devices/platform", "/sys/class/gpio", "/soc/"]

# Install dependencies
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.7 && apt-get install -y python3-pip

# Install application dependencies
RUN python3.7 -m pip install -r requirements.txt && python3.7 setup.py install

CMD python3.7 -m nucuhub.sensors.main