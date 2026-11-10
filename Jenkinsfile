pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install dependencies') {
            steps {
                bat '"C:\\Users\\2303a\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv .venv'
                bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                bat '.venv\\Scripts\\python -m pytest -q --junitxml=test-results/results.xml'
            }
        }
        stage('Build Docker image') {
            steps {
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" build -t contractflow:%BUILD_NUMBER% .'
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results/*.xml'
        }
    }
}