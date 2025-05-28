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
    command: ['cat']
    tty: true
  - name: docker
    image: docker:24.0.6
    command: ['cat']
    tty: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock
  - name: kubectl
    image: bitnami/kubectl:1.30.0
    command: ['sh', '-c', 'sleep infinity']
    tty: true
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
    }
  }

  // triggers {
  //   pollSCM('* * * * *')
  // }

  stages {
    stage('Test python') {
      steps {
        container('python') {
          sh 'pip install -r requirements.txt'
          sh 'python test.py'
        }
      }
    }

    stage('Start Registry') {
      steps {
        container('docker') {
          sh '''
            if [ -z "$(docker ps -q -f name=registry)" ]; then
              docker run -d -p 4000:5000 --name registry registry:2
            fi
          '''
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

    stage('Deploy') {
      steps {
        container('kubectl') {
          sh 'which kubectl'
          sh 'kubectl version --client=true'
          sh 'kubectl apply -f ./kubernetes/deployment.yaml'
          sh 'kubectl apply -f ./kubernetes/service.yaml'
        }
      }
    }
  }
}