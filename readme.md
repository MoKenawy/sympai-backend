# SympAI Backend

<image src="https://github.com/MoKenawy/sympai-backend/blob/main/docs/symp-ai-logo.jfif" width="100%" height="500px"/>

## Overview
SympAI Backend provides the core API services for the SympAI healthcare chatbot, which assists users in identifying symptoms and receiving preliminary medical advice. The backend is built using FastAPI, integrated with natural language processing (NLP) models, and is containerized for easy deployment.
<image src="https://github.com/MoKenawy/sympai-backend/blob/main/docs/API-0.png"/>

  </br>
  <hr>



This repository works together with the [SympAI Frontend](https://github.com/MoKenawy/sympai-front), which provides the web-based user interface.
  </br>

<image src="https://github.com/MoKenawy/sympai-backend/blob/main/docs/Context-Diagram_Level_0.svg" />


## Features
- FastAPI-based API for handling chatbot queries.
- Integration with pre-trained medical NLP models (BioMistral 7B, Meditron 7B).
- Support for multi-turn conversations using LangChain.
- Dockerized for ease of deployment and scaling.
- Deployed on AWS EC2 with API Gateway and Load Balancer.

  </br>
<image src="https://github.com/MoKenawy/sympai-backend/blob/main/docs/aws%20solution_V3.drawio.png"/>


## Installation

### Prerequisites
- Docker
- Python 3.12
- AWS CLI (for deployment)
- Ollama (for running the NLP models locally)

### Install dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/symp-ai-backend.git
   cd symp-ai-backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Set up environment variables:
Set the necessary environment variables for deployment:
   ```bash
   export AWS_ACCESS_KEY_ID= <your aws_access_key_id>
   export AWS_SECRET_ACCESS_KEY= <your aws_secret_access_key>
   export INIT_PATHS_DIR="/app/src"
   export AWS_REGION="us-east-1"
   export FRONT_URL="http://localhost:3000"  # Link to the frontend
   export OLLAMA_BASE_URL="http://localhost:11434"
   ```


## Run Docker to containerize the backend:
1. Build the Docker image:
   ```bash
   docker build -t sympai-backend .
   ```

1. Run the container:
   ```bash
   docker run -p 8000:8000 sympai-backend
   ```

## License
This project is licensed under the [MIT License](https://github.com/MoKenawy/sympai-backend/blob/main/LICENSE).

# Related Repositories
[SympAI Frontend](https://github.com/MoKenawy/sympai-front)
