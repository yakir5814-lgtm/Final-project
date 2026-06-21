# Final Project: Python Microservice & Infrastructure Management

This repository contains the source code, containerization logic, and CI pipeline configuration for my final project, which focuses on automated infrastructure and microservice deployment.

## 🛠 Project Components
* **Application Code (`app.py`):** A Python-based microservice designed for deployment in a containerized environment.
* **Dockerfile:** Defines the container image build process, ensuring a consistent environment for the Python application.
* **Jenkins Pipeline (`Jenkinsfile`):** Automates the Continuous Integration (CI) process. It builds the Docker image and pushes it to Docker Hub upon every code change.
* **Helm Charts:** Managed configurations for deploying the application reliably on Kubernetes.

## 🚀 CI/CD Workflow
1. **Source Code:** Managed here, in the `Final-project` repository.
2. **CI (Jenkins):** Jenkins detects changes, runs builds, and pushes the new image to [yakirmehager/final-project](https://hub.docker.com/r/yakirmehager/final-project).
3. **CD (Argo CD):** A separate GitOps repository monitors these changes and triggers automatic deployment to the Kubernetes cluster.

## 📂 Key Files
* `app.py`: The main application logic.
* `Dockerfile`: Instructions to build the application container.
* `Jenkinsfile`: The automation script for the CI pipeline.
* `requirements.txt`: Python dependencies required for the service.

## 📊 Status
* **Development/Production:** Managed through continuous deployment pipelines.
* **Builds:** Automated via Jenkins.

---
*Developed as part of a comprehensive DevOps Final Project.*
