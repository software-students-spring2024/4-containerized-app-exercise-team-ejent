![Python build & test](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-ejent/actions/workflows/ml.yml/badge.svg) 

# Containerized Emotion Tracker App

## Description

The Containerized Emotion Tracker App is a web application designed to help users track their emotions over time. The app allows users to log their emotions at different times throughout the day and provides visualizations to help users understand their emotional patterns. The app is built with Python and is containerized using Docker for easy deployment and scalability.

## Configuration

To run the Containerized Emotion Tracker App, you will need to have Docker installed on your machine. Once Docker is installed, you can clone the repository and build the Docker image:

```bash
git clone https://github.com/software-students-spring2024/4-containerized-app-exercise-team-ejent.git
cd 4-containerized-app-exercise-team-ejent
docker build -t emotion-tracker-app .

```

After the Docker image is built, you can run the app with the following command:


docker run -p 8000:8000 emotion-tracker-app


Teammates
Jean Luis Adrover: https://github.com/jladrover

Sang In Harry Kang: https://github.com/sik247

Ellis Pinsky: https://github.com/ellispinsky

