def get_stash_name(docker_image, create_args) {
    return "bi-${docker_image}-${create_args}".replaceAll('/','-')
}

def lockfile_name(docker_image, create_args) {
    return "${get_stash_name(docker_image, create_args)}.lock"
}

def get_stages(docker_image, artifactory_name, artifactory_repo, create_args) {
    return {
        node {
            docker.image(docker_image).inside("--net=docker_jenkins_artifactory") {
                def server = Artifactory.server artifactory_name
                def client = Artifactory.newConanClient()
                client.run(command: "remote clean")
                def remoteName = client.remote.add server: server, repo: artifactory_repo
                def lockfile = lockfile_name(docker_image, create_args)

                try {
                    client.run(command: "config set general.default_package_id_mode=full_version_mode")
                    client.run(command: "config set general.revisions_enabled=1")

                    stage("${docker_image}") {
                        echo 'Running in ${docker_image}'
                    }

                    stage("Get project") {
                        checkout scm
                    }

                    stage("Get dependencies and create app") {
                        String arguments = "${create_args} --lockfile=${lockfile}"
                        client.run(command: "graph lock . ${arguments}".toString())
                        client.run(command: "create . sword/sorcery ${arguments}".toString())
                        sh "cat ${lockfile}"
                    }

                    stage("Upload packages") {
                        String uploadCommand = "upload core-messages* --all -r ${remoteName} --confirm"
                        client.run(command: uploadCommand)
                    }

                    stage("Stash lockfile") {
                        def stash_name = get_stash_name(docker_image, create_args)
                        echo "Stash '${stash_name}' -> '${lockfile}'"
                        stash name: stash_name, includes: "${lockfile}"
                    }
                }
                finally {
                    deleteDir()
                }
            }
        }
    }
}

def artifactory_name = "Artifactory Docker"
def artifactory_repo = "conan-local"
def docker_images = ["conanio/gcc8", "conanio/gcc7"]
def create_args_list = ["-s compiler.libcxx=libstdc++", "-s compiler.libcxx=libstdc++11"]

def stages = [:]
docker_images.each { docker_image ->
    create_args_list.each { create_args ->
        stages[docker_image + " " + create_args] = get_stages(docker_image, artifactory_name, artifactory_repo, create_args)
    }
}

node {
    try {
        stage("Build + upload") {
            parallel stages
        }

        stage("Retrieve build info") {
            docker.image("conanio/gcc8").inside("--net=docker_jenkins_artifactory") {
                def buildInfo = Artifactory.newBuildInfo()
                String artifactory_credentials = "http://artifactory:8081/artifactory,admin,password"

                // Install helper script (WIP)
                git url: 'https://gist.github.com/a39acad525fd3e7e5315b2fa0bc70b6f.git'
                sh 'pip install rtpy'

                String python_command = "python lockfile_buildinfo.py --remotes=${artifactory_credentials}"
                python_command += " --build-number=${buildInfo.getNumber()} --build-name=\"${buildInfo.getName()}\""
                python_command += " --multi-module"

                docker_images.each { docker_image ->
                    create_args_list.each { create_args ->
                        def stash_name = get_stash_name(docker_image, create_args)
                        unstash stash_name
                        python_command += " " + lockfile_name(docker_image, create_args)
                    }
                }

                echo python_command
                sh python_command
                sh "ls -la ${pwd()}"
                sh "cat buildinfo.json"

                // Publish build info
                String publish_command = "python publish_buildinfo.py --remote=${artifactory_credentials} buildinfo.json"
                sh publish_command
            }
        }
    }
    finally {
        deleteDir()
    }
}
