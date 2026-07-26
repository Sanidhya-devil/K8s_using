pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')   // Jenkins credential ID
        IMAGE_NAME = 'yourdockerhubusername/cicd-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        DEPLOY_SERVER = 'ec2-user@your-server-ip'                // used in Deploy stage
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Pulling latest code from repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Logging in and pushing image to Docker Hub...'
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container to target server...'
                sh '''
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_SERVER} '
                        docker pull ${IMAGE_NAME}:latest &&
                        docker stop cicd-flask-app || true &&
                        docker rm cicd-flask-app || true &&
                        docker run -d --name cicd-flask-app -p 80:5000 ${IMAGE_NAME}:latest
                    '
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully. App deployed!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
        always {
            sh 'docker logout || true'
        }
    }
}
