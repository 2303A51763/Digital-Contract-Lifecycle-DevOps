pipeline {
    agent any
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install dependencies') {
            steps { sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt' }
        }
        stage('Test') {
            steps { sh '. .venv/bin/activate && pytest -q' }
        }
        stage('Build Docker image') {
            steps { sh 'docker build -t contractflow:${BUILD_NUMBER} .' }
        }
    }
    post {
        always { junit allowEmptyResults: true, testResults: 'test-results/*.xml' }
    }
}
