pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/PalashDS/Price_forecasting_application.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --junitxml=results.xml'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application...'
                // Add build steps, if applicable, like compiling or packaging code
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                // Deploy to a server, upload to cloud, etc.
            }
        }
    }

    post {
        always {
            junit 'results.xml'  // Archiving test results
            archiveArtifacts artifacts: '**/results.xml', allowEmptyArchive: true
        }
    }
}
