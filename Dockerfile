FROM python:3.9.6

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python3", "app.py"]