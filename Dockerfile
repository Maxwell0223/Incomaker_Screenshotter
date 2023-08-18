# Start with CentOS 8 base image
FROM ubuntu:22.04

# Install required system packages

# Install Chrome if installChrome is set to true
#ARG installChrome=true
#COPY google-chrome/google-chrome-stable-102.0.5005.61-1.x86_64.rpm /tmp/google-chrome-stable-102.0.5005.61-1.x86_64.rpm
#COPY selenium/chromedriver /opt/selenium/chromedriver
RUN apt update -y \
    && apt install python3 -y \ 
    && apt install python3-pip -y
    #&& yum install /tmp/google-chrome-stable-102.0.5005.61-1.x86_64.rpm -y \
    #&& rm -f /tmp/google-chrome-stable-102.0.5005.61-1.x86_64.rpm

# Switch to the app directory
WORKDIR /app

# Install Python dependencies
COPY app/requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt \
    && pip3 install webdriver-manager \
    && apt install wget -y \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb

# Run app.py as the final command
CMD ["python3", "app.py"]
