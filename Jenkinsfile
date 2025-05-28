pipeline {
  agent {
    kubernetes {
      label 'jenkins-agent-my-app'
      yaml '''
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
    - name: docker
      image: docker:24.0.6
      command:
        - cat
      tty: true
      volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
'''
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

    stage('Build image') {
      steps {
        container('docker') {
          sh 'docker build -t localhost:4000/flask_hello:latest .'
          sh 'docker push localhost:4000/flask_hello:latest'
        }
      }
    }
  }
}
