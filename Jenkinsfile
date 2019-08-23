def get_stash_name(docker_image) {
    return "bi-${docker_image}".replaceAll('/','-')
}

def get_stages(docker_image, artifactory_name, artifactory_repo) {
    return {
        node {
            docker.image(docker_image).inside("--net=docker_jenkins_artifactory") {
                def server = Artifactory.server artifactory_name
                def client = Artifactory.newConanClient()
                def remoteName = client.remote.add server: server, repo: artifactory_repo

                stage("${docker_image}") {
                    echo 'Running in ${docker_image}'
                }

                stage("Get project") {
                    checkout scm
                }

                stage("Get dependencies and create app") {
                    client.run(command: "create . sword/sorcery")
                }

                stage("Upload packages") {
                    String uploadCommand = "upload core-messages* --all -r ${remoteName} --confirm"
                    def buildInfo = client.run(command: uploadCommand)
                    // server.publishBuildInfo buildInfo
                    // TODO: We need to join the buildInfo of these jobs...
                }

                stage("Stash build info") {
                    def stash_name = get_stash_name(docker_image)
                    echo "Stash '${stash_name}' -> '${client.getLogFilePath()}'"

                    sh "ls -la ${pwd()}"
                    git url: 'https://gist.github.com/601afe655ea2577d5f0ac8bc4035bdc6.git'
                    sh "ls -la ${pwd()}"

                    dir(client.getUserPath()) {
                        //sh "ls -la ${pwd()}"
                        stash name: stash_name, includes: "conan_log.log"
                    }
                }
            }
        }
    }
}

def artifactory_name = "Artifactory Docker"
def artifactory_repo = "conan-local"
//def docker_images = ["conanio/gcc8", "conanio/gcc7"]
def docker_images = ["conanio/gcc8"]

def stages = [:]
docker_images.each { docker_image ->
    stages[docker_image] = get_stages(docker_image, artifactory_name, artifactory_repo)
}

node {
    stage("Build + upload") {
        parallel stages
    }

    stage("Retrieve build info") {
        docker.image("conanio/gcc8").inside("--net=docker_jenkins_artifactory") {
            def server = Artifactory.server artifactory_name
            def client = Artifactory.newConanClient()
            def buildInfo = client.run(command: '--version')

            docker_images.each { docker_image ->
                def stash_name = get_stash_name(docker_image)
                echo "Unstash '${stash_name}'"
                dir(client.getUserPath()) {
                    unstash stash_name
                    sh "ls -la ${pwd()}"
                    client.run(command: '--version', buildInfo: buildInfo)
                }
            }

            server.publishBuildInfo buildInfo
        }
    }
}
