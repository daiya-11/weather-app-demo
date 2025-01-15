# Project Name

This project involves setting up a web server using Python to proxy requests to the public OpenWeather API. The application is containerized using Docker and connected to a MongoDB database via Docker. Docker Compose is used to run the services locally. A Kubernetes cluster on GCP GKE is used to orchestrate the solution in the cloud. The project includes configuring multiple environments (dev, staging, production) using Kustomize, setting up Ingress for external access. Additionally, a Kubernetes CronJob is implemented to rotate credentials (username and password) and ensure zero downtime during reconnections. The project was deployed on the GKE cluster in the staging environment.

To access the application, visit the following link:
[weather-app-staging.34.116.165.112.nip.io/](http://weather-app-staging.34.116.165.112.nip.io/)

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Usage](#usage)

## Introduction

This project is a simple weather application built using Python and Flask that allows users to fetch real-time weather data for any city using the OpenWeather API. The application retrieves weather information such as temperature and weather descriptions.

The project integrates several modern technologies:

MongoDB: Weather data is stored in MongoDB, allowing the retrieval of historical weather information.
Docker: The application is containerized with Docker.
Kubernetes: The application is orchestrated using Kubernetes, ensuring reliability and scalability across different environments (dev, staging, production).
Kustomize: Environment-specific configurations are managed with Kustomize, enabling seamless deployments across multiple clusters.
Security: Kubernetes secrets are used to manage database credentials, and a Kubernetes CronJob is implemented to rotate credentials automatically for security and ensure zero downtime during reconnections.

## Features

- Real-Time Weather Data: Fetch current weather data for any city using the OpenWeather API, including temperature, weather description.

- Data Persistence in MongoDB: Store and retrieve weather data from MongoDB, ensuring that weather history is available for future queries.

- MongoDB Integration: Connect securely to MongoDB using Kubernetes secrets to manage database credentials, ensuring sensitive information is protected.

- Kubernetes Orchestration: The application is deployed in a GKE cluster, providing scalability, high availability, and easy updates.

- Multi-Environment Support with Kustomize: Use Kustomize to manage configurations for different Kubernetes environments (dev, staging, production), making the application adaptable to multiple environments.

Database Credential Rotation with Kubernetes CronJob: A Kubernetes CronJob automatically rotates database credentials (username and password) every minute, ensuring secure access to MongoDB and preventing downtime during credential changes.

Ingress: Ingress is configured to manage external access to the application, ensuring secure communication between services and pods.

Easy Setup and Deployment: The application is fully containerized with Docker, simplifying both local setup using Docker Compose and deployment to a Kubernetes cluster.

## Technologies

This project utilizes the following technologies:

- Python 3.x: The primary programming language for the backend.
- Flask: A lightweight web framework for building the web server.
- OpenWeather API: A public API used to fetch real-time weather data.
- MongoDB: A NoSQL database for storing weather data.
- Docker: Containerization tool for packaging the application and its dependencies.
- Docker Compose: A tool for defining and running multi-container Docker applications. It’s used for running MongoDB and the Flask app locally during development.
- JavaScript: JavaScript scripts are used for database initialization within Docker Compose, helping set up the MongoDB database with initial data during container startup.
- Bash Scripting: Bash scripts are used for various configuration tasks, including setting up the database and managing environment variables.
- Google Kubernetes Engine (GKE): A managed Kubernetes service from Google Cloud Platform (GCP) used for deploying, managing, and scaling the application in a Kubernetes cluster.
- Google Cloud Platform (GCP) Artifact Registry: A fully-managed service to store and manage Docker images in GCP, used for storing the application container images.
- Kustomize: A tool for managing Kubernetes configurations across multiple environments.
- This project uses [nip.io](https://nip.io/) as free free DNS.

## Installation

Follow these steps to set up the project locally and run it:

### 1. Clone the repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/daiya-11/weather-app-demo.git
```

### 2. Set up environment variables

Create a `.env` file in the project /src directory and add the required environment variables. Make sure to replace the placeholders with your actual values:

```bash
API_KEY=<your-openweather-api-key>
MONGO_USER=<your-mongo-username>
MONGO_PASSWORD=<your-mongo-password>
```

### 3. Set up Docker and Docker Compose

This project uses Docker to containerize the application. Follow these steps to get Docker up and running:

1. **Install Docker**: If you don’t have Docker installed, follow the instructions on [Docker’s website](https://docs.docker.com/get-docker/) for your operating system.

2. **Build the Docker Image Locally**:

   Navigate to the /src directory of the project and build the Docker image with the following command:

   ```bash
   docker build -t weather-app-demo:v1.0.1 .
   ```

3. **Install Docker Compose**: If you don’t have Docker Compose installed, follow the instructions on [Docker Compose installation](https://docs.docker.com/compose/install/).

4. **Build and run the application with Docker Compose**:

   Once Docker and Docker Compose are installed, run the following command to start the MongoDB service and the Flask app locally:

   ```bash
   docker compose up --build
   ```

   This will build the Docker images and start the services defined in the `docker-compose.yml` file, including MongoDB and the Flask app.

### 4. Verify local setup

Once the application is running, it will be accessible at `http://localhost:5000`. You can verify that the app is working by visiting this URL and using the available routes (`/weather`, `/weather_from_db`).

### 5. Setting up GKE and Artifact Registry

To deploy the project on Google Kubernetes Engine (GKE), follow these additional steps:

1. **Set up Google Cloud SDK**: Install the Google Cloud SDK and authenticate your account.

   [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

2. **Create a GKE Cluster**:

   Create a GKE cluster in the Google Cloud Console or use the following command:

   ```bash
   gcloud container clusters create app-staging --zone europe-central2-a --num-nodes=2
   ```

3. **Push Docker Image to GCP Artifact Registry**:

   - Build and tag the Docker image:

   ```bash
   docker build -t gcr.io/your-project-id/weather-app-demo:v1 .
   ```

   - Push the image to the Artifact Registry:

   ```bash
   docker push gcr.io/your-project-id/weather-app:v1
   ```

4. **Deploy to GKE**:

   This project uses **Kustomize** for Kubernetes deployments. Follow the steps below to deploy the application using Kustomize:

   1. **Install Kustomize**:

      To install **Kustomize**, follow the instructions on the official GitHub page:

      [Install Kustomize](https://github.com/kubernetes-sigs/kustomize/releases)

      Choose the appropriate method for your operating system from the release page.

   2. **Customize the Manifests**:

      After installing Kustomize, customize the Kubernetes manifests with your configuration:

      - Update the `image` name, environment variables, or any other settings in the manifests located in the /kubernetes/ directory according to your setup.

   3. **Deploy the Application**:

      After customizing the manifests, you can deploy the application using the following command:

      ```bash
      kubectl apply -k kubernetes/weather-app-demo/overlay/staging
      ```

   4. **Verify Deployment**:

      Once the deployment is successful, check the status of your pods with:

      ```bash
      kubectl get pods
      ```

### 6. Kubernetes Ingress and CronJob Setup

You can also configure **Ingress** to manage external traffic and set up a **CronJob** for rotating database credentials as mentioned in the project details.

#### 1. **Ingress Setup**:

In order to expose the application externally, you need to configure an **Ingress**. Follow these steps:

1.1 **Update the Ingress Manifests**:

The Ingress manifest file is located in the /kubernetes/ directory. Open this file and customize it to match your environment. If you are using a dynamic DNS solution, update the `host` field with your desired DNS name.


1.2 **Apply the Ingress Configuration.**

1.3 **Verify external access:**
Once deployed, you can access the application on host. Use the following command to get host:

```bash
kubectl get ingress
```

Visit the host to verify that the app is running.

#### 2. **CronJob Setup**:

1.1 **Update the CronJob Manifests**

The CronJob manifest file is located in the /kubernetes/ directory. Open this file and customize it to match your environment.

2.2 **Apply the CronJob Configuration.**

### 7. Using nip.io for DNS

This project uses [nip.io](https://nip.io/) for dynamic DNS management. You can easily access the deployed services by using `nip.io` with the external IP of your service.

For example, if your service is exposed with an external IP of `12.34.56.78`, you can access it via the URL: http://12-34-56-78.nip.io

## Usage

To access the application, visit the following link:
weather-app-staging.34.116.165.112.nip.io/

### API Endpoints

The following endpoints are available in the Weather app:

#### 1. Home Route

- **Endpoint**: `GET /`
- **Description**: Returns a welcome message for the Weather app.
- **Response**:
  ```json
  {
    "message": "Welcome to the Weather app demo!"
  }
  ```

#### 2. Get Weather Data

- **Endpoint**: `GET /weather`
- **Description**: Fetches weather data for a specified city from the OpenWeather API.
- **Query Parameters**:
  - `city` (required): Name of the city for which you want to get the weather data.
- **Example Request**:
  ```
  GET /weather?city=London
  ```
- **Response**:
  ```json
  {
    "city": "London",
    "temperature": 15.5,
    "description": "light rain"
  }
  ```

#### 3. Get Weather Data from Database

- **Endpoint**: `GET /weather_from_db`
- **Description**: Retrieves all weather data that has been stored in MongoDB.
- **Response**:
  ```json
  [
    {
      "city": "London",
      "temperature": 15.5,
      "description": "light rain",
      "timestamp": 1609459200
    },
    {
      "city": "Paris",
      "temperature": 18.0,
      "description": "clear sky",
      "timestamp": 1609459200
    }
  ]
  ```
  ***
