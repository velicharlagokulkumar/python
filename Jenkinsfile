pipeline {
  agent any
  stages {
    stage('2') {
      parallel {
        stage('1.1') {
          steps {
            echo '2'
          }
        }

        stage('2.1') {
          steps {
            echo '2.1'
          }
        }

      }
    }

    stage('3') {
      parallel {
        stage('1.2') {
          steps {
            echo '3'
          }
        }

        stage('2.2') {
          steps {
            echo '2.2'
          }
        }

      }
    }

  }
}