FROM public.ecr.aws/docker/library/python:3.12.4-slim

WORKDIR /app
EXPOSE 8000

RUN apt-get update && apt-get install -y curl
RUN curl -LO https://github.com/k8sgpt-ai/k8sgpt/releases/download/v0.3.40/k8sgpt_amd64.deb
RUN dpkg -i k8sgpt_amd64.deb

RUN  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]