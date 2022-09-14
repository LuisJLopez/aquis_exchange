FROM python:3.9.5

# Set working directory
WORKDIR /app

# Install modules
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Add source code to working dir
ADD . /app

# Run
CMD ["python", "project/__main__.py"]
