def appname = "final-project"
def repo = "yakirmehager"
def appimage = "docker.io/" + repo + "/" + appname
def apptag = env.BUILD_NUMBER

podTemplate(cloud: 'kubernetes', containers: [
    containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent:latest'),
    containerTemplate(name: 'docker', image: 'docker:26-dind', privileged: true, args: '--storage-driver=vfs'),
    containerTemplate(name: 'kubectl', image: 'bitnami/kubectl:latest')
    ],
    volumes: [emptyDirVolume(mountPath: '/var/lib/docker', memory: false)]) {
    
    node(POD_LABEL) {
        stage('Checkout') {
            container('jnlp') {
                checkout scm
            }
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
       stage('Update GitOps Repo') {
    container('jnlp') {
        // כאן אתה צריך להגדיר Credentials ל-GitHub ב-Jenkins
        sshagent(['github-ssh-key']) {
            sh '''
                git clone git@github.com:yakir5814-lgtm/gitops.git
                cd gitops/apps
                # עדכון גרסת ה-Image בקובץ ה-YAML
                sed -i "s|image: .*|image: ${appimage}:${apptag}|g" nginx-deployment.yaml
                git config user.email "jenkins@jenkins.com"
                git config user.name "Jenkins"
                git add .
                git commit -m "Update image to ${apptag}"
                git push origin main
            '''
        }
    }
}
            }
        }
        stage('Done') {
            container('jnlp') {
                echo "Pipeline finished!"
            }
        }
    }
}
