FROM python:3.9-alpine
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["py_github_cli"]
