FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
RUN pip install flask
RUN echo "FLAG{c0mm4nd_1nj3ct10n_r3uss1}" > /flag.txt
COPY app.py .
CMD ["python", "app.py"]
