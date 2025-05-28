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
  - name: tools
    image: ubuntu:22.04
    command: ['cat']
    tty: true
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
    }
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

    stage('Install kubectl') {
      steps {
        container('tools') {
          sh '''
            apt-get update -qq
            apt-get install -y curl
            curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
            chmod +x kubectl
            mv kubectl /usr/local/bin/
          '''
        }
      }
    }

    stage('Deploy') {
      steps {
        container('tools') {
          sh 'kubectl version --client=true'
          sh 'kubectl apply -f ./kubernetes/deployment.yaml'
          sh 'kubectl apply -f ./kubernetes/service.yaml'
        }
      }
    }
  }
}