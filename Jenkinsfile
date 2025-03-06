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
                    docker.build("haniyatariq65/mlops-assignment:${env.BUILD_ID}")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("haniyatariq65/mlops-assignment:${env.BUILD_ID}").push()
                    }
                }
            }
        }
    }
    post {
        success {
            emailext body: 'The build was successful!', subject: 'Build Success', to: 'aiyza.junaid@gmail.com'
        }
    }
}