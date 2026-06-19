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
        stage('Deploy') {
            container('jnlp') {
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    script {
                        // 1. שכפול ה-Repo (שימוש ב-single quotes מונע את אזהרת האבטחה)
                        sh 'git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/yakir5814-lgtm/gitops.git'
                        
                        // 2. חיפוש הקובץ כדי לוודא נתיב
                        sh "find . -name deployment.yaml"
                        
                        // 3. עדכון הקובץ עם בדיקת קיום
                        // החלפתי ל-dir דינמי בהתאם למציאות של הקובץ אם התיקייה משתנה
                        dir('gitops/apps') {
                            if (fileExists('deployment.yaml')) {
                                sh "sed -i 's|image:.*|image: ${appimage}:${apptag}|g' deployment.yaml"
                                
                                // 4. commit ו-push
                                sh '''
                                    git config user.email "jenkins@jenkins.com"
                                    git config user.name "Jenkins"
                                    git add deployment.yaml
                                    git commit -m "Update image to ${apptag}"
                                    git push origin main
                                '''
                            } else {
                                error "deployment.yaml not found in gitops/apps!"
                            }
                        }
                    }
                }
            }
        }
        stage('Done') {
            echo "Pipeline finished!"
        }
    }
}
