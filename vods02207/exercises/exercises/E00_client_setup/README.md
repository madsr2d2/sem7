[//]: # "__RELEASE_REMOVE_TOTAL__"

# Project setup

- Instructions to set up WSL and Docker is handed out as PDF.

## Directory structure

    ```bash
    client_setup/
    │── scripts                         # Scripts related with Docker and WSL
    │   ├── Dockerfile
    │   └── setup_wsl.sh                # Setup WSL for the first time
    ├── README.md
    ├── setup_command_build.sh
    ├── setup_command_run.sh
    ```


## Docker Setup
This will describe the details of the docker setup

### Dockerfile
The following describe some details of the Dockerfile

**USER ID**
The user ID and group ID is set by the following arguments:
```
ARG USER_UID=1000
ARG USER_GID=1000
```
When using docker in WSL it is enough to keep these as is, but when running on `sscs02`, these must correspond to that of the user.
This ensures that we have write access inside the folder mounted in docker.

**COPY FILE INTO CONTAINER**
To put a file into the container when building it the following command can be used
```
COPY <file> <location>/<file>
```

### Docker Commands

**docker build**

Docker build is based on the info in the `Dockerfile` and requires the ubuntu-22.04 image.

The build-command used in the client-setup is as follows:
(Note: `  is the escape character used in Windows Powershell)

```
docker build `
-f Dockerfile `
--target builder-icarus `
--tag syosil-icarus-img `
--target syosil-base `
--build-arg USERNAME=$env:username-docker `
--tag syosil-ubuntu-container `
. ; `
docker image prune -f
```

Running the build-commmand builds two images: `syosil-icarus-img` and `syosil-ubuntu-container`.
`docker image prune` removes unused images.

ubuntu-22.04 has Python 3.10 pre-installed and it is used for the project.

`syosil-icarus-img` handles download and installation of icarus.
`syosil-ubuntu-container` is the main image and handles setting up the user repository and settings.


**docker run**
Running a docker container has the following format `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

The run-command used in the client-setup is as follows:
```
docker run -it `
-v ("<C:\Users\WINDOWS-USERNAME\Documents\syosil-project>" +
    ":/home/" + $env:username + "-docker/<syosil-project>") `
-e DISPLAY=<IP_ADDRESS>:0.0 `
--name syosil-ubuntu-container `
syosil-ubuntu-container
```

**OPTIONS**
Some important options for the run command are:

* `-i` interactive, means we can write in the terminal
* `-t` a pseudo-TTY
* `--rm` the container is removed on exit
* `-v` mounting local files into docker. Uses format `-v <HOST_PATH>:<CONTAINER_PATH>`

Another option is specifying an input file following the run-command as:
```
# in Powershell
docker run [...] /home/$env:username-docker/file.sh

# in Makefile
docker run [...] /home/${USERNAME}$/file.sh
```
This overrides the `CMD`or `ENTRYPOINT` specified in the docker image and the file is being run instead. The file must be the specified by the whole path.