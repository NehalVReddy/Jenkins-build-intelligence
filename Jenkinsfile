pipeline {
    agent any

    environment {
        JENKINS_URL = "http://localhost:8080"
        JOB_NAME    = "Jenkins_Build_Intelligence"
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

        stage('Run Build Intelligence') {
            steps {
                withCredentials([
                    string(credentialsId: 'jenkins-build-intelligence', variable: 'API_TOKEN'),
                    string(credentialsId: 'jenkins-build-intelligence', variable: 'USERNAME')
                ]) {
                    bat """
                    docker run --rm ^
                    -e JENKINS_URL=%JENKINS_URL% ^
                    -e JOB_NAME=%JOB_NAME% ^
                    -e USERNAME=%USERNAME% ^
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
