apt-get update
apt-get install -y software-properties-common
apt-get install -y python-software-properties
apt-get install -y curl
apt-get install -y apt-transport-https

curl -s https://bootstrap.pypa.io/get-pip.py | python3 -

python -m pip install -r /vagrant/requirements.txt

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
apt-get update
apt-get install -y docker-ce
