FROM python:3.10.0

WORKDIR /tezis_jobber/tezis_medo_manager-master/

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]