def appname = "final-project"
def repo = "yakirmehager"
def appimage = "docker.io/" + repo + "/" + appname
def apptag = env.BUILD_NUMBER

podTemplate(cloud: 'kubernetes', containers: [
    containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent:latest'),
    containerTemplate(name: 'docker', image: 'docker:26-dind', privileged: true, args: '--storage-driver=vfs'),
    containerTemplate(name: 'kubectl', image: 'bitnami/kubectl:latest', command: 'cat', ttyEnabled: true)
    ],
    volumes: [emptyDirVolume(mountPath: '/var/lib/docker', memory: false)]) {
    
    node(POD_LABEL) {
        
        stage('Checkout') {
            container('jnlp') { checkout scm }
        }

        stage('Build') {
            container('docker') {
                sh "docker build -t ${appimage}:${apptag} ."
            }
        }

        stage('Push') {
            container('docker') {
                withCredentials([usernamePassword(credentialsId: 'my-login-secret', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh "docker push ${appimage}:${apptag}"
                }
            }
        }

        stage('Deploy') {
            container('kubectl') {
                script {
                    def namespace = "default" 
                    def deploymentName = "nginx"
                    
                    try {
                        // מוודא שה-Deployment קיים לפני שמנסים לעדכן
                        sh "kubectl get deployment/${deploymentName} -n ${namespace}"
                        sh "kubectl set image deployment/${deploymentName} ${deploymentName}=${appimage}:${apptag} -n ${namespace}"
                    } catch (Exception e) {
                        echo "DEPLOY FAILED! Check if deployment '${deploymentName}' exists in namespace '${namespace}'"
                        throw e
                    }
                }
            }
        }

        stage('Done') {
            container('jnlp') { echo "Pipeline finished!" }
        }
    }
}
