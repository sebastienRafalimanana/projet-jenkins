pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent-my-app'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: ci
spec:
  containers:
    - name: python
      image: python:3.10.12
      command:
        - cat
      tty: true
"""
        }
    }
    triggers {
      pollSCM('* * * * *')
    }
    stages {
        stage('Test python') {
            steps {
                container('python') {
                    sh 'pip install -r requirements.txt'
                    sh 'python test.py'
                }
            }
        }
    }
}
