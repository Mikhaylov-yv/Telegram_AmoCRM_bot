FROM python:3.9.12-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./scr .
CMD [ "python", "./start_bot.py" ]