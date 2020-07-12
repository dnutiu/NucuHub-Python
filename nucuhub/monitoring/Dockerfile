# To build this image use the following command:
# docker build . -f ./nucuhub/monitoring/Dockerfile -t nucuhub.sensors
# To debug: docker run -it nucuhub.monitoring /bin/bash
FROM python:3.7-buster
MAINTAINER Denis Nutiu

WORKDIR app

# Copy the NucuHub folder into the workdir
COPY . .

# Install application dependencies
RUN python3 -m pip install -r requirements.txt

CMD python3 -m nucuhub.monitoring.main