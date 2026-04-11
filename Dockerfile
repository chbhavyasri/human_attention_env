FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1

# The validator expects the server on port 8000
EXPOSE 8000

# This command starts the server for the 'Reset' check
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]