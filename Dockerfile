FROM python:3.12
WORKDIR /dockerWD
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./pasta-man.py"]