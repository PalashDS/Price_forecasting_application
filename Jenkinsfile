pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "streamlit_app"
        APP_PORT = "8501"
    }

    tools {
        dockerTool 'docker' // Use the Docker tool configured in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sameersharmaAI/casestudy2'
            }
        }

        stage('Setup Virtual Environment and Install Dependencies') {
            steps {
                // Create virtual environment and install dependencies
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests/
                '''
            }
        }

        stage('Build Docker Image with Ansible') {
            steps {
                sh '''
                . venv/bin/activate
                ansible-playbook -i localhost, -c local playbook.yml --tags build
                '''
            }
        }

        stage('Stop Existing Container with Ansible') {
            steps {
                sh '''
                . venv/bin/activate
                ansible-playbook -i localhost, -c local playbook.yml --tags stop
                '''
            }
        }

        stage('Deploy Application with Ansible') {
            steps {
                sh '''
                . venv/bin/activate
                ansible-playbook -i localhost, -c local playbook.yml --tags deploy
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            sh 'rm -rf venv'  // Remove the virtual environment after the pipeline
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
