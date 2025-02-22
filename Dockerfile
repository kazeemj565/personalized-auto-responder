# Use a lightweight Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port and run app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
