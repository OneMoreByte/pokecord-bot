FROM ubuntu:latest

# Update and install deps

RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-pip
RUN useradd -ms /bin/bash bot
RUN touch /usr/bin/chatter
RUN chown bot:bot /usr/bin/chatter
RUN chmod +x /usr/bin/chatter
# Switch to user
USER bot
RUN python3 -m pip install -U discord.py

# Set defaults for parameters
ENV TOKEN=""
ENV WAKE=8
ENV SLEEP=12
ENV WPM=80

ADD ./chatter.py /usr/bin/chatter
ADD ./dialog /movies
ENTRYPOINT ["python3", "-u", "/usr/bin/chatter"]
