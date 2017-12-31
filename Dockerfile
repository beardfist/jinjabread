FROM ubuntu:16.04

# Add code to container
ADD src /
ADD requirements.txt /


# Prerequisites
RUN apt-get update
RUN apt-get install -y software-properties-common \
                       python-software-properties \
                       curl \
                       apt-transport-https

RUN curl -s https://bootstrap.pypa.io/get-pip.py | python3 -

# Install requirements
RUN python3 -m pip install -r requirements.txt

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 80
ENTRYPOINT ["gunicorn", "-w", "4", "--worker-connections", "1000", "--timeout", "120", "-b", "0.0.0.0:80", "jinjabread:app"]
