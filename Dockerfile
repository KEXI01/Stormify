FROM nikolaik/python-nodejs:python3.10-nodejs19
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app/
COPY . /app/
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
CMD ["python3", "-m", "Opus"]