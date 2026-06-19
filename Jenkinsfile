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
                // שימוש ב-withCredentials בצורה בטוחה כדי למנוע את ה-Warning
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    script {
                        sh 'rm -rf gitops'
                        // שימוש בסינטקס בטוח למניעת חשיפת הסוד
                        sh 'git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/yakir5814-lgtm/gitops.git'
                        
                        // דיבג: הצגת מבנה התיקיות כדי לראות איפה הקבצים שלך באמת
                        sh 'find gitops -maxdepth 3'
                        
                        // מציאת קובץ ה-deployment.yaml בכל מקום בתוך התיקייה
                        def targetFile = sh(script: 'find gitops -name "deployment.yaml" | head -n 1', returnStdout: true).trim()
                        
                        if (targetFile == "") {
                            error "לא נמצא קובץ בשם deployment.yaml בתוך ה-Repository!"
                        }
                        
                        echo "נמצא קובץ בנתיב: ${targetFile}"
                        
                        // עדכון ה-Image
                        sh "sed -i 's|image:.*|image: ${appimage}:${apptag}|g' ${targetFile}"
                        
                        // ביצוע Commit ו-Push
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
