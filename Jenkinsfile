// 1. Loading the shared library must be at the very first line of the file
@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('Hello') {
            steps { 
                echo 'Hello World' 
            }
        }

        stage('Get Source Control') {
            steps { 
                echo 'Cloning repository...' 
            }
        }

        stage('Close SCM') {
            steps { 
                echo 'Cleaning workspace...' 
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
                stage('Bandit scan') { 
                    steps { 
                        echo 'Running Bandit...' 
                    } 
                }
                stage('Docker Build') { 
                    steps { 
                        echo 'Building Docker...' 
                    } 
                }
                
                // 2. השלב המעודכן שמריץ את הסורק הרשמי בצורה נקייה ויציבה
                stage('Sonarqube') { 
                    steps { 
                        echo 'Analyzing code quality via official SonarQube Scanner...'
                        script {

                            def scannerHome = tool 'SonarQubeScanner'
                            
                            withSonarQubeEnv('SonarQubeScanner') {
                                sh """
                                    ${scannerHome}/bin/sonar-scanner \
                                    -Dsonar.projectKey=my-app \
                                    -Dsonar.projectName=my-app \
                                    -Dsonar.sources=. \
                                    -Dsonar.sourceEncoding=UTF-8
                                """
                            }
                        }
                    } 
                }
                
                stage('Trivy scan') { 
                    steps { 
                        echo 'Scanning for vulnerabilities...' 
                    } 
                }
            }
        }

        stage('Docker push and Tests (Parallel)') {
            when { expression { env.ACTION == 'Proceed' } }
            parallel {
                stage('Secure Docker push') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'my-login-secret', 
                                                         usernameVariable: 'DOCKER_USER', 
                                                         passwordVariable: 'DOCKER_PASS')]) {
                            script {
                                echo "Pushing image with user: ${env.DOCKER_USER}"
                                sh "echo Logging in with \$DOCKER_USER"
                            }
                        }
                    }
                }
                stage('End to end test') { 
                    steps { 
                        echo 'Running E2E tests...' 
                    } 
                }
                stage('Integrity test') { 
                    steps { 
                        echo 'Checking integrity...' 
                    } 
                }
                stage('unit test') { 
                    steps { 
                        echo 'Running unit tests...' 
                    } 
                }
            }
        }

        stage('Create Artifact') {
            when { expression { env.ACTION == 'Proceed' } }
            steps {
                sh 'echo "Finalizing" > final.txt'
                archiveArtifacts artifacts: 'final.txt', allowEmptyArchive: true
            }
        }

        stage('Continue the pipeline') {
            when { expression { env.ACTION == 'Proceed' } }
            steps { 
                echo 'Success!' 
            }
        }

        stage('Abort the Pipeline') {
            when { expression { env.ACTION == 'Abort' } }
            steps { 
                error 'Pipeline stopped' 
            }
        }

        stage('Finalize the Pipeline') {
            steps { 
                echo 'Done' 
            }
        }
    }
}
