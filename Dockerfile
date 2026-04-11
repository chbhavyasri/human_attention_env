FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
# Runs the entry point we defined in pyproject.toml
CMD ["server"]