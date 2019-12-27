pipeline {
         agent any
         stages {
                 stage('Build') {
                     steps {
                         echo 'Build pyhidentity'
                         sh 'pip3 install -r requirements.txt'
                         sh 'python3 setup.py bdist_wheel'
                         sh 'sudo python3 setup.py install'
                     }
                 }
                 stage('Test') {
                    steps {
                        echo 'Test pyhidentity'
                        sh 'python3 -m unittest discover pyhidentity/test/ -v'
                    }
                 }
                 stage('Deploy') {
                    steps {
                        echo "Deploy pyhidentity to target server"
                        sshPublisher(publishers: [sshPublisherDesc(configName: 'christian@server', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'sudo pip3 install projects/pyhidentity/$BUILD_NUMBER/pyhidentity-*.whl', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: 'pyhidentity/$BUILD_NUMBER', remoteDirectorySDF: false, removePrefix: 'dist', sourceFiles: 'dist/*.whl')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
                    }
                }
    }
}
