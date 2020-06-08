# To build this image use the following command:
# docker build . -f ./nucuhub/sensors/Dockerfile -t nucuhub.sensors
# To debug: docker run -it nucuhub.sensors /bin/bash
FROM python:3.7-slim
MAINTAINER Denis Nutiu

WORKDIR app

# Copy the NucuHub folder into the workdir
COPY . .

# Share the volumes; Used to access GPIO ports.
VOLUME ["/sys/class/thermal/", "/sys/devices/platform", "/sys/class/gpio", "/soc/"]

# Install application dependencies
RUN python3 -m pip install -r requirements.txt && python3 setup.py install

CMD python3 -m nucuhub.sensors.main