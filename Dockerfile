FROM python:3.10.0-alpine3.15

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# TODO maybe create main src/ folder?
COPY blockchain/ blockchain/
COPY coin/ coin/
COPY errors/ errors/
COPY utils/ utils/
COPY app.py .

EXPOSE 5000

COPY bin/ bin/

CMD ["/app/bin/start-server.sh"]
