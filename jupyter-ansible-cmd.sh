#!/bin/bash
set +e

message() {
    echo "Please run:" >&2
    echo "            $0 build      " >&2
    echo "            $0 run        " >&2
}

build_rootfs() {
    tar -C ./rootfs/ -zcvf rootfs.tar.gz .
}

build_img() {
    build_rootfs;

    build_date=$(date +%Y%m%d%H%M%S)
    docker images --quiet --filter=dangling=true | xargs --no-run-if-empty docker rmi

    echo "Building jupyter-ansible image"

    docker build -t wallacechendockerhub/jupyter-ansible:latest . --no-cache -f Dockerfile
}

create_persistent_volume() {
    rcmvol=$(docker volume ls -q|grep -w jupyter-ansible-data)

    if [[ "$rcmvol" == "jupyter-ansible-data" ]]; then
        echo "volume: jupyter-ansible-data is ready!"
    else
        echo "volume: jupyter-ansible-data is not ready, create it!"
        docker volume create jupyter-ansible-data
    fi
}

run_ja() {
    echo "Running ja container"

    create_persistent_volume;
    docker run --name ja --net=host \
        --restart unless-stopped \
        --mount 'type=volume,src=jupyter-ansible-data,dst=/var/lib/jupyter-ansible,volume-driver=local' \
        -v /etc/localtime:/usr/share/zoneinfo/DefZone:ro \
        -v /var/run/docker.sock:/var/run/docker.sock \
        --privileged=true \
        -e TZ=$(readlink /etc/localtime) \
        -u root -idt wallacechendockerhub/jupyter-ansible:latest
}

<<COMMENT
MULTILINE COMMAND
COMMENT

case "$1" in
    build)
        sleep 1
        if [ "$#" -ne 1 ]; then
            message;
            exit 1
        fi
	build_img;
        ;;
    run)
        sleep 1
        if [ "$#" -ne 1 ]; then
            message;
            exit 1
        fi
	run_ja;
        exit 0
        ;;
    *)
        message;
        exit 1
        ;;
esac
exit 100
