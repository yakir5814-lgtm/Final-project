def appname = "final-project"
def repo = "yakirmehager"
def appimage = "docker.io/" + repo + "/" + appname
def apptag = env.BUILD_NUMBER

podTemplate(cloud: 'kubernetes', containers: [
    containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent:latest'),
    containerTemplate(name: 'docker', image: 'docker:26-dind', privileged: true, args: '--storage-driver=vfs')
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
            container('jnlp') {
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    script {
                        // 1. הורדת ה-GitOps Repo
                        sh 'rm -rf gitops'
                        sh 'git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/yakir5814-lgtm/gitops.git'
                        
                        // 2. מציאת הקובץ באופן אוטומטי (לא משנה איפה הוא ב-Repo)
                        def yamlFile = sh(script: 'find gitops -name "*.yaml" | head -n 1', returnStdout: true).trim()
                        
                        if (yamlFile == "") {
                            error "לא נמצא אף קובץ YAML ב-Repository!"
                        }
                        
                        echo "מעדכן את הקובץ: ${yamlFile}"
                        
                        // 3. עדכון ה-Image בתוך הקובץ
                        sh "sed -i 's|image:.*|image: ${appimage}:${apptag}|g' ${yamlFile}"
                        
                        // 4. שליחת השינויים חזרה ל-GitHub
                        dir('gitops') {
                            sh '''
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
            container('jnlp') { echo "Pipeline finished!" }
        }
    }
}
