#!/bin/bassh


if [ -z "$1" ]; then echo "No directory specified"; exit; fi
install_dir=$1

echo "Parsing google apis..."

json_data=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json)
stable_version=$(echo $json_data | jq -r '.channels.Stable.version')
unset json_data

echo "Latest version from channel stable: "$stable_version
echo "Installing to "$install_dir

# https doesn't work (idk why)
wget -q "http://storage.googleapis.com/chrome-for-testing-public/"$stable_version"/linux64/chromedriver-linux64.zip"
wget -q "http://storage.googleapis.com/chrome-for-testing-public/"$stable_version"/linux64/chrome-linux64.zip"

mkdir -p $install_dir

unzip -qq -o chrome-linux64.zip -d bin
unzip -qq -o chromedriver-linux64.zip -d bin

echo "Chrome and chromedriver version "$stable_version" installed to folder "$install_dir", cleaning up"

rm chrome-linux64.zip*
rm chromedriver-linux64.zip*