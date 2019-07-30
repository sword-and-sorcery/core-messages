
def get_stages(docker_image, artifactory_name, artifactory_repo) {
    return {
        docker.image(docker_image).inside('--net=docker_jenkins_artifactory') {
            def server = Artifactory.server artifactory_name
            def client = Artifactory.newConanClient()
            def remoteName = client.remote.add server: server, repo: artifactory_repo

            stage("Get project") {
                checkout scm
            }

            stage("Get dependencies and create app") {
                client.run(command: "create . sword/sorcery")
            }

            stage("Upload packages") {
                String uploadCommand = "upload core-messages* --all -r ${remoteName} --confirm"
                def buildInfo = client.run(command: uploadCommand)
                server.publishBuildInfo buildInfo
            }
        }
    }
}

def artifactory_name = "Artifactory Docker"
def artifactory_repo = "conan-local"
def docker_images = ["conanio/gcc8", "conanio/gcc7"]

node {
    def stages = [:]

    docker_images.each { docker_image ->
        stages[docker_image] = get_stages(docker_image, artifactory_name, artifactory_repo)
    }
    
    parallel stages
}
