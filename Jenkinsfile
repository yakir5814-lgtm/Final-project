def appname = "final-project"
def repo = "yakirmehager"
def appimage = "docker.io/" + repo + "/" + appname
def apptag = env.BUILD_NUMBER

podTemplate(cloud: 'kubernetes', 
    containers: [
        containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent:latest'),
        containerTemplate(
            name: 'docker', 
            image: 'docker:26-dind', 
            privileged: true,
            ttyEnabled: true,
            command: 'dockerd-entrypoint.sh'
        )
    ],
    volumes: [
        emptyDirVolume(mountPath: '/var/lib/docker', memory: false)
    ]) {
    
    node(POD_LABEL) {
        stage('Checkout') {
            container('jnlp') {
                checkout scm
            }
        }
        
        stage('Build') {
            container('docker') {
                script {
                    timeout(time: 30, unit: 'SECONDS') {
                        waitUntil {
                            def result = sh(script: 'docker info', returnStatus: true)
                            return result == 0
                        }
                    }
                }
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
        
        stage('Update GitOps Repo') {
            container('jnlp') {
                // שימוש ב-Credentials של HTTPS במקום SSH
                withCredentials([usernamePassword(credentialsId: 'github-pat-secret', usernameVariable: 'GH_USER', passwordVariable: 'GH_TOKEN')]) {
                    sh """
                        rm -rf gitops
                        git clone https://${GH_USER}:${GH_TOKEN}@github.com/${repo}/gitops.git
                        
                        cd gitops/apps
                        
                        sed -i "s|image: .*|image: ${appimage}:${apptag}|g" nginx-deployment.yaml
                        
                        git config user.email jenkins@jenkins.com
                        git config user.name Jenkins
                        git add nginx-deployment.yaml
                        git commit -m "Update image to ${apptag}"
                        git push https://${GH_USER}:${GH_TOKEN}@github.com/${repo}/gitops.git main
                    """
                }
            }
        }
        
        stage('Done') {
            container('jnlp') {
                echo "Pipeline finished! ArgoCD will sync automatically now."
            }
        }
    }
}
