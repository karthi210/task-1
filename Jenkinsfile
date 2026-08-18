pipeline {
    agent any
    
    stages {
        stage('code') {
            steps {
                git branch: 'main', url: 'https://github.com/karthi210/task-1.git'
            }
        }
        stage('clean port') {
            steps {
                sh '''
                docker ps -q --filter "publish=5000" | xargs -r docker rm -f
                '''
            }
        }
        stage('build image') {
            steps {
                sh '''
                docker build -t image .
                '''
            }
        }
        stage('run image') {
            steps {
                sh '''
                docker run -d -p 5000:5000 image
                '''
            }
        }
    }
}
