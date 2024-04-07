#!/bin/sh

create_docker_volume() {
    local volume_name=$1
    
    if ! docker volume inspect "$volume_name" >/dev/null 2>&1; then
        echo "Creating docker volume:"
        docker volume create "$volume_name"
    fi
}

create_docker_volume palpa-py-bash-history
create_docker_volume palpa-py-vscode-extensions
