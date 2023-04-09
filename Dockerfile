FROM python:3.10-slim
COPY requirements.txt ./requirements.txt
CMD cat requirements.txt
RUN pip install -r requirements.txt
COPY . ./
CMD [ "python3" , "app/app.py" ]