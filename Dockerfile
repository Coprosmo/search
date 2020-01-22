FROM python:3.8

COPY . .
RUN pip install -r requirements.txt

CMD python -m src.search.__main__ 
