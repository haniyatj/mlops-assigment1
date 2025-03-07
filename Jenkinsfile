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

        stage('Send Email') {
            steps {
                script {
                    // Write a Python script to send email
                    writeFile file: 'send_email.py', text: '''
                    import smtplib
                    from email.mime.text import MIMEText

                    sender = "aiyza.junaid@gmail.com"
                    receiver = "haniya911@gmail.com"
                    subject = "Build Success"
                    body = "The Jenkins build was successful!"

                    msg = MIMEText(body)
                    msg["Subject"] = subject
                    msg["From"] = sender
                    msg["To"] = receiver

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login("haniya911@gmail.com", "xmeg uleu mxfl cwpt")
                        server.sendmail(sender, receiver, msg.as_string())
                    '''
                    // Run the Python script
                    sh 'python3 send_email.py'
                }
            }

    }

}