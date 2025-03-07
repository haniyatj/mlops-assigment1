pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Check Branch') {
            steps {
                script {
                    if (env.GIT_BRANCH != 'origin/main') {
                        error("This pipeline only runs for merges to the main branch.")
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("aiyza/mlops-assignment:${env.BUILD_ID}")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image("aiyza/mlops-assignment:${env.BUILD_ID}").push()
                    }
                }
            }
        }

        stage('Check curl') {
            steps {
                script {
                    // Check if curl is installed
                    sh 'curl --version'
                }
            }
        }

        stage('Send Email') {
            steps {
                script {
                    // Send email using curl and SMTP
                    sh '''
                        curl --url "smtps://smtp.gmail.com:465" \
                             --ssl-reqd \
                             --mail-from "aiyza.junaid@gmail.com" \
                             --mail-rcpt "haniya911@gmail.com" \
                             --user "haniya911@gmail.com:xmeg uleu mxfl cwpt" \
                             --upload-file - <<EOF
                        From: Jenkins <aiyza.junaid@gmail.com>
                        To: haniya911@gmail.com
                        Subject: Build Success

                        The Jenkins build was successful!
                        EOF
                    '''
                }
            } 
        }

    }


}