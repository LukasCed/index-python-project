FROM python:3.4-alpine
ADD . .
WORKDIR .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]