# To build this image use the following command:
# docker build . -f ./nucuhub/sensors/Dockerfile -t nucuhub.sensors
# To debug: docker run -it nucuhub.sensors /bin/bash
FROM python:3.7-buster
MAINTAINER Denis Nutiu

WORKDIR app

# Copy the NucuHub folder into the workdir
COPY . .

# Share the system volume.
VOLUME ["/sys"]

# Install application dependencies
RUN python3 -m pip install -r requirements.txt && python3 -m pip install -r ./nucuhub/sensors/requirements.txt

CMD python3 -m nucuhub.sensors.main