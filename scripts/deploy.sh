#! /bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

echo "deploy-ios.sh"

if [[ "$TRAVIS_PULL_REQUEST" != "false" ]]; then
  echo "This is a pull request. No deployment will be done."
  exit 0
fi
if [[ "$TRAVIS_BRANCH" != "deploy" ]]; then
  echo "Testing on a branch other than deploy. No deployment will be done."
  exit 0
fi

export GITHUB_USER='JrGoodle'
export GITHUB_REPO='clowder'

cd "${TRAVIS_BUILD_DIR}"

echo 'Create source distribution'
echo '--------------------------'
python3 setup.py sdist
echo ''

echo 'Create wheel'
echo '------------'
python3 setup.py bdist_wheel

SETUP_PY="${TRAVIS_BUILD_DIR}/setup.py"
VERSION=$(awk "/version='/" "${SETUP_PY}" | sed -n -e "s/^.*version='//p" | tr -d "',")
echo "VERSION=${VERSION}"
TAG="v${VERSION}"

if git rev-list "${TAG}" >/dev/null; then
	echo "${TAG} tag exists."
else
    echo "${TAG} tag not found. Creating new tag and GitHub Release"
    # Create new tag
    git tag "${TAG}"
    git push origin "${TAG}"
    # Create new GitHub Release from tag
    github-release release \
        --tag "${TAG}" \
        --name "${TAG}" \
		--description "Release ${TAG}"

    cd "${TRAVIS_BUILD_DIR}/dist"

    artifacts=( "clowder-${VERSION}-py3-none-any.whl" \
                 "clowder-${VERSION}.tar.gz" )

    for artifact in "${artifacts[@]}"; do
        echo "Upload ${artifact} to GitHub Release"
        github-release upload \
            --tag "${TAG}" \
            --name "${artifact}" \
            --file "${artifact}"
    done
fi
