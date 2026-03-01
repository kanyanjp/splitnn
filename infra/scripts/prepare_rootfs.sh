set -euo pipefail

DOCKER_IMAGE_NAME=${1:-}
RUNTIME_DIR=${2:-}

if [ -z "${DOCKER_IMAGE_NAME}" ]; then
    echo "DOCKER_IMAGE_NAME not set, exiting..."
    exit 1
fi

for cmd in podman skopeo umoci; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
        echo "Missing required command: ${cmd}"
        exit 1
    fi
done

WORK_DIR=$(dirname "$(readlink -f "$0")")/../
if [ -z "${RUNTIME_DIR}" ]; then
    TMP_DIR="${WORK_DIR}/runtime"
else
    TMP_DIR="${RUNTIME_DIR}"
fi

IFS=":" read -r DOCKER_IMAGE_REPO DOCKER_IMAGE_TAG <<< "${DOCKER_IMAGE_NAME}"
if [ -z "${DOCKER_IMAGE_TAG}" ]; then
    DOCKER_IMAGE_TAG="latest"
fi

IMAGE_LAYERS_DIR="${TMP_DIR}/img_layers"
IMAGE_BUNDLES_DIR="${TMP_DIR}/img_bundles"
IMAGE_LAYER_DIR="${IMAGE_LAYERS_DIR}/${DOCKER_IMAGE_REPO}"
IMAGE_OVERLAYFS_DIR="${IMAGE_BUNDLES_DIR}/${DOCKER_IMAGE_REPO}/${DOCKER_IMAGE_TAG}"
IMAGE_ROOTFS_DIR="${IMAGE_OVERLAYFS_DIR}/rootfs"

if [ -d "${IMAGE_ROOTFS_DIR}" ]; then
    echo "Rootfs cache of ${DOCKER_IMAGE_NAME} is available"
    echo "Image rootfs is stored at: ${IMAGE_ROOTFS_DIR}"
    exit 0
fi

echo "Rootfs cache of ${DOCKER_IMAGE_NAME} is unavailable, extracting rootfs..."
mkdir -p "${IMAGE_LAYER_DIR}" "${IMAGE_OVERLAYFS_DIR}"

# Podman-managed image workflow (default).
if ! podman image exists "${DOCKER_IMAGE_NAME}"; then
    echo "Pulling image with podman: ${DOCKER_IMAGE_NAME}"
    podman pull "${DOCKER_IMAGE_NAME}"
fi
skopeo copy "containers-storage:${DOCKER_IMAGE_NAME}" "oci:${IMAGE_LAYER_DIR}:${DOCKER_IMAGE_TAG}"
rm -rf "${IMAGE_OVERLAYFS_DIR}"
umoci unpack --image "${IMAGE_LAYER_DIR}:${DOCKER_IMAGE_TAG}" "${IMAGE_OVERLAYFS_DIR}"

if [ ! -d "${IMAGE_ROOTFS_DIR}" ]; then
    echo "Image rootfs creation failed! Exiting..."
    exit 1
fi
echo "Image rootfs is stored at: ${IMAGE_ROOTFS_DIR}"
