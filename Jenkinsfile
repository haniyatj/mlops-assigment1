pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build("your-dockerhub-username/mlops-assignment:${env.BUILD_ID}")
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("your-dockerhub-username/mlops-assignment:${env.BUILD_ID}").push()
                    }
                }
            }
        }
    }
    post {
        success {
            emailext body: 'The build was successful!', subject: 'Build Success', to: 'admin@example.com'
        }
    }
}