pipeline {
    agent any

    environment {
        IMAGE_NAME  = "jenkins-build-intelligence"
        JENKINS_URL = "http://host.docker.internal:8080"
        JOB_NAME    = "jenkins-check"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/NehalVReddy/jenkins-build-intelligence.git',
                    credentialsId: 'github-pat-new'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Run Container (SERVICE MODE)') {
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_TOKEN')
                ]) {
                    bat '''
                    docker rm -f demo || true
                    docker run -d ^
                      --name demo ^
                      -p 5000:5000 ^
                      -e JENKINS_URL=http://host.docker.internal:8080 ^
                      -e JOB_NAME=jenkins-check ^
                      -e USERNAME=admin ^
                      -e API_TOKEN=%API_TOKEN% ^
                      jenkins-build-intelligence
                    '''
                }
            }
        }

        stage('List Running Containers') {
            steps {
                bat 'docker ps'
            }
        }
    }
}
