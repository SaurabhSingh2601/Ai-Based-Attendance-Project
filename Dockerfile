FROM python:3.11-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CMAKE_BUILD_PARALLEL_LEVEL=1

# Install system dependencies required for opencv, audio, and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    libsndfile1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and setuptools (pinned to <81 to keep pkg_resources support)
RUN pip install --no-cache-dir --upgrade pip "setuptools<81.0.0" wheel

# 1. Install lightweight CPU-only PyTorch first (avoids downloading 3.5GB of NVIDIA CUDA wheels on Render)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 2. Install remaining requirements (dlib-bin will now use pre-compiled Linux binary wheel in 2 seconds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy application code
COPY . .

# Expose Render default port
EXPOSE 8501

# Run Streamlit on Render dynamically reading $PORT
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false"]
