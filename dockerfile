FROM python:latest
RUN apt-get update && apt-get -y install cron
RUN pip install azure-storage-blob
RUN pip install pyyaml
RUN mkdir /app
ADD backup-cron /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron
WORKDIR /app
ADD backup.py /app/backup.py
CMD ["cron", "-f"]
#CMD [ "python3", "./backup.py"]