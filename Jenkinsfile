pipeline {
    agent any

    environment {
        JENKINS_URL = "http://host.docker.internal:8080"
        JOB_NAME    = "jenkins-check"
        IMAGE_NAME  = "jenkins-build-intelligence"
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
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('List Docker Images') {
            steps {
                bat "docker images"
            }
        }

        stage('Run Build Intelligence (Batch Job)') {
            steps {
                withCredentials([
                    string(credentialsId: 'api-key', variable: 'API_TOKEN')
                ]) {
                    bat """
                    docker run --rm ^
                    -e JENKINS_URL=%JENKINS_URL% ^
                    -e JOB_NAME=%JOB_NAME% ^
                    -e USERNAME=admin ^
                    -e API_TOKEN=%API_TOKEN% ^
                    -v %WORKSPACE%:/output ^
                    %IMAGE_NAME%
                    """
                }
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: '*.json', fingerprint: true
            }
        }
    }
}
