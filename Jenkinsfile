pipeline {
    agent {
        docker {
          image 'ghcr.io/ziv-gabel/tshark-python3:latest'
        }
      }
    parameters {
        file(name: 'uploaded_file', description: 'Upload the file to process')
    }
    environment {
        SCRIPT = 'extract_tshark_data.sh'
    }
    stages {
        stage('Prepare File') {
            steps {
                script {
                    // Unstash the uploaded file
                    unstash 'uploaded_file'
                }
            }
        }
        stage('Run Script on Runner Node') {
            steps {
                script {
                    sh """
                    chmod +x ${WORKSPACE}/${SCRIPT}
                    ${WORKSPACE}/${SCRIPT} ${WORKSPACE}/uploaded_file
                    """
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline succeeded. Archiving artifacts...'
            archiveArtifacts artifacts: 'aggregated_*', allowEmptyArchive: true
        }
        always {
            cleanWs()
            echo 'Pipeline execution completed.'
        }
    }
}