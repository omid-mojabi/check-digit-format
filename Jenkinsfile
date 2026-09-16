pipeline {
    agent any

    environment {
        VENV = '.venv'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    mkdir -p reports
                    pytest --cov=src --cov-report=xml --cov-report=term
                '''
            }
            post {
                always {
                    junit 'reports/pytest.xml'
                }
            }
        }
    }

    post {
        cleanup {
            cleanWs()
        }
    }
}
