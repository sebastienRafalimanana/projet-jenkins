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

    stage('Check files') {
      steps {
        container('tools') {
          sh 'ls -la'
          sh 'find . -name "*.yaml" -o -name "*.yml"'
        }
      }
    }

    stage('Deploy') {
      steps {
        container('tools') {
          sh 'kubectl version --client=true'
          script {
            // Vérifier si les fichiers existent avant de les appliquer
            if (fileExists('./kubernetes/deployment.yaml')) {
              sh 'kubectl apply -f ./kubernetes/deployment.yaml'
            } else if (fileExists('./k8s/deployment.yaml')) {
              sh 'kubectl apply -f ./k8s/deployment.yaml'
            } else if (fileExists('./deployment.yaml')) {
              sh 'kubectl apply -f ./deployment.yaml'
            } else {
              error 'Fichier deployment.yaml non trouvé'
            }
            
            if (fileExists('./kubernetes/service.yaml')) {
              sh 'kubectl apply -f ./kubernetes/service.yaml'
            } else if (fileExists('./k8s/service.yaml')) {
              sh 'kubectl apply -f ./k8s/service.yaml'
            } else if (fileExists('./service.yaml')) {
              sh 'kubectl apply -f ./service.yaml'
            } else {
              error 'Fichier service.yaml non trouvé'
            }
          }
        }
      }
    }
  }
}