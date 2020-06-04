#!/bin/bash

IMAGE_NAME="bonjourmadame-api-server"

if [ ! -z "${DOCKER_USERNAME}" ]; then
    # maintainer
    echo "Build type: maintainer"
    docker pull ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
    docker build --cache-from ${DOCKER_USERNAME}/${IMAGE_NAME}:latest -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${TRAVIS_COMMIT} .
    docker tag ${DOCKER_USERNAME}/${IMAGE_NAME}:${TRAVIS_COMMIT} ${DOCKER_USERNAME}/${IMAGE_NAME}:nightly
else
    # other
    echo "Build type: other"
    docker build -t local/${IMAGE_NAME}:${TRAVIS_COMMIT}
fi

docker container run -d --name ${IMAGE_NAME} -p 5000:5000 ${DOCKER_USERNAME:-local}/${IMAGE_NAME}:${TRAVIS_COMMIT}
sleep 10
docker ps | grep ${IMAGE_NAME} && echo "Container running successfully"
curl -sL http://127.0.0.1:5000/ | egrep "Return a latest url picture for bonjourmadame" && echo "BonjourMadame API Server running successfully"
docker logs ${IMAGE_NAME}
