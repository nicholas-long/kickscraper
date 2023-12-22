FROM python:3.12-bullseye

WORKDIR /app
ADD requirements.txt .
ADD scrape_user.py .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/app/scrape_user.py" ]
