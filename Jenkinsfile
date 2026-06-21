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
                sshagent(['github-ssh-key']) {
                    sh """
                        # שיבוט הריפו של ה-GitOps (מומלץ לוודא שהתיקייה לא קיימת מהרצה קודמת)
                        rm -rf gitops
                        git clone git@github.com:${repo}/gitops.git
                        cd gitops/apps
                        
                        # שימוש במשתנים שהגדרנו למעלה כדי לעדכן את האימג'
                        sed -i "s|image: .*|image: ${appimage}:${apptag}|g" nginx-deployment.yaml
                        
                        git config user.email jenkins@jenkins.com
                        git config user.name Jenkins
                        git add nginx-deployment.yaml
                        git commit -m "Update image to ${apptag}"
                        git push origin main
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
