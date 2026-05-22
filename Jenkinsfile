@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('Hello') {
            steps { 
                echo 'Hello World' 
            }
        }

        stage('Wait for User Approval') {
            steps {
                script {
                    def userInput = input message: 'Ready to build?',
                                         parameters: [choice(name: 'Option', choices: 'Proceed\nAbort')]
                    env.ACTION = userInput
                }
            }
        }

        stage('Build in Parallel') {
            when { expression { env.ACTION == 'Proceed' } }
            parallel {
                stage('Bandit scan') { steps { echo 'Running Bandit...' } }
                stage('Docker Build') { steps { echo 'Building Docker...' } }
                stage('Trivy scan') { steps { echo 'Scanning...' } }
            }
        }

        stage('Finalize the Pipeline') {
            steps { echo 'Done' }
        }
    }
}
