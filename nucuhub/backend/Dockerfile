# To build this image use the following command:
# docker build . -f ./nucuhub/backend/Dockerfile -t nucuhub.backend
# To debug: docker run -it nucuhub.backend /bin/bash
FROM python:3.7-buster
MAINTAINER Denis Nutiu

WORKDIR app

# Copy the NucuHub folder into the workdir
COPY . .

# Install application dependencies
RUN python3 -m pip install -r requirements.txt && python3 -m pip install -r ./nucuhub/backend/requirements.txt

CMD python3 -m nucuhub.backend.main