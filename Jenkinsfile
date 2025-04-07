pipeline {
    agent any

    triggers {
        githubPush()  
    }

    environment {
        PACKAGE = "nclient pandas ipaddress netaddr prettytable"
        SCRIPT = "netman_netconf_obj2.py"
        TEST = "unit_test_netman.py"
    }

    stages {

        stage('Package Installs') {
            steps {
                echo 'Installing nccclient pandas ipaddress netaddr prettytable...'
                script {
                    def libs = env.PACKAGE.split()
                    for (lib in libs) {
                        sh """
                        if ! python3 -c "import ${lib}" &> /dev/null; then
                            echo "Installing ${lib}..."
                            pip3 install ${lib}
                        else
                            echo "${lib} already installed."
                        fi
                        """
                    }
                }
            }
        }

        stage('Code Style Check with pylint') {
            steps {
                echo 'Checking code style using pylint...'
                sh """
                pip3 install pylint
                pylint --fail-under=5 ${SCRIPT}
                """
            }
        }

        stage('Run Application') {
            steps {
                echo 'Running netman_netconf_obj2.py...'
                sh "python3 ${SCRIPT}"
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh """
                pip3 install -U unittest-xml-reporting
                python3 -m unittest ${TEST}
                """
            }
        }
    }

    post {
        success {
            echo 'Build succeeded!'
            mail to: 'pranav.deepak1608@gmail.com',
                 subject: "✅ Jenkins Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Great job! Your Jenkins build was successful."
        }

        failure {
            echo 'Build failed!'
            mail to: 'pranav.deepak1608@gmail.com',
                 subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Oops! The Jenkins build failed. Check the logs for details."
        }
    }
}