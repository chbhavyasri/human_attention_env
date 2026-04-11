FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
# Hugging Face defaults to 7860, Scaler might use 8000. 
# We use the PORT variable provided by the host.
ENV PORT=7860

EXPOSE 7860

# This command runs the server on the port Hugging Face assigns
CMD uvicorn main:app --host 0.0.0.0 --port $PORT