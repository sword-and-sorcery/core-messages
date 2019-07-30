
def get_stages(docker_image, artifactory_name, artifactory_repo) {
    return {
        docker.image(docker_image).inside('--net=docker_jenkins_artifactory') {
            def server = Artifactory.server artifactory_name
            def client = Artifactory.newConanClient()
            def remoteName = client.remote.add server: server, repo: artifactory_repo

            stage("${docker_image}") {
                echo 'Running in ${docker_image}'
            }

            stage("Get dependencies and create app") {
                client.run(command: "create . sword/sorcery")
            }

            stage("Upload packages") {
                String uploadCommand = "upload core-messages* --all -r ${remoteName} --confirm"
                def buildInfo = client.run(command: uploadCommand)
                // server.publishBuildInfo buildInfo
                // TODO: We need to join the buildInfo of these jobs...
                stash name: "bi-${docker_image}".replaceAll('/','-'), includes: client.getLogFilePath()
            }
        }
    }
}

def artifactory_name = "Artifactory Docker"
def artifactory_repo = "conan-local"
def docker_images = ["conanio/gcc8", "conanio/gcc7"]

node {
    stage("Get project") {
        checkout scm
    }

    def stages = [:]
    docker_images.each { docker_image ->
        stages[docker_image] = get_stages(docker_image, artifactory_name, artifactory_repo)
    }

    stage("Build + upload") {
        parallel stages
    }

    stage("Retrieve build info") {
        docker_images.each { docker_image ->
            echo "docker_image: ${docker_image}"
            unstash "bi-${docker_image}".replaceAll('/','-')
        }
    }
}
