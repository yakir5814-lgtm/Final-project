def appname = "final-project"
def repo = "yakirmehager"
def appimage = "docker.io/" + repo + "/" + appname
def apptag = env.BUILD_NUMBER

pipeline {
    agent {
        kubernetes {
            yaml """
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:latest
  - name: docker
    image: docker:26-dind
    privileged: true
    args: ['--storage-driver=vfs']
  volumes:
  - name: docker-sock
    emptyDir: {}
"""
        }
    }
    tools {
        git 'Default' // שימוש בכלי ה-Git שהגדרת ב-Jenkins
    }
    stages {
        stage('Checkout') {
            steps {
                container('jnlp') {
                    checkout scm
                }
            }
        }
        stage('Build') {
            steps {
                container('docker') {
                    sh "docker build -t ${appimage}:${apptag} ."
                }
            }
        }
        stage('Push') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(credentialsId: 'my-login-secret', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                        sh "docker push ${appimage}:${apptag}"
                    }
                }
            }
        }
        stage('Update GitOps Repo') {
            steps {
                container('jnlp') {
                    sshagent(['github-ssh-key']) {
                        sh '''
                            git clone git@github.com:yakir5814-lgtm/gitops.git
                            cd gitops/apps
                            # מעדכן את האימג' בקובץ ה-YAML שנמצא ב-Repo של ה-gitops
                            sed -i "s|image: .*|image: ${appimage}:${apptag}|g" nginx-deployment.yaml
                            git config user.email "jenkins@jenkins.com"
                            git config user.name "Jenkins"
                            git add nginx-deployment.yaml
                            git commit -m "Update image to ${apptag}"
                            git push origin main
                        '''
                    }
                }
            }
        }
        stage('Done') {
            steps {
                container('jnlp') {
                    echo "Pipeline finished! ArgoCD will sync automatically now."
                }
            }
        }
    }
}
