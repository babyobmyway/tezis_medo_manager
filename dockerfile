FROM python:3.10.0

WORKDIR /tezis_jobber

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]