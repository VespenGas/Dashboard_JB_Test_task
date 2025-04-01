FROM python:3.12.9
ENV LANG=C.UTF-8

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8855
ENTRYPOINT ["python", "main.py"]
