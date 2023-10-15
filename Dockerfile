FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-12.py310
FROM python:3.8-slim
RUN pip install tensorflow google-cloud-storage

RUN pip install -U scikit-learn


WORKDIR /app
COPY . .
ENTRYPOINT ["python"]
CMD ["./Prediction.py"]
