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

        // stage('Run Container') {
        //     steps {
        //         bat '''
        //         docker run --rm jenkins-build-intelligence
        //         // docker run -d --name jenkins-build-intelligence -p 5000:5000 %IMAGE_NAME%
        //         '''
        //     }
        // }
        
        stage('List Docker Images') {
            steps {
                bat "docker images"
            }
        }


        stage('Run Build Intelligence') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'jenkins-api',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'API_TOKEN'
                    )
                ]) {
                    bat """
                    docker run --rm ^
                    -e JENKINS_URL=http://host.docker.internal:8080 ^
                    -e JOB_NAME=jenkins-check ^
                    -e USERNAME=%USERNAME% ^
                    -e API_TOKEN=%API_TOKEN% ^
                    -v %WORKSPACE%:/output ^
                    jenkins-build-intelligence
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
