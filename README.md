# lakehouse
Lakehouse using Iceberg &amp; MinIO

## Setup for Raspberry Pi 4B:

SSH into the node:
``` bash
ssh user@host.local
```
Update and upgrade node:
``` bash
sudo apt update
sudo apt full-upgrade -y
```
Get docker
``` bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
Lets add our user for ir
``` bash
sudo usermod -aG docker $USER
```
And then apply the changes
``` bash
su - ${USER}
```

Then we can test the intsallation
``` bash
docker run hello-world
```


## Docker compose
``` bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

```

``` bash
git clone https://github.com/datador/lakehouse.git
cd lakehouse
```
Create the relevant environment variables
``` bash
nano .env

```

``` bash
docker-compose up -d

```

## Venv

``` bash
python3 -m venv env
source env/bin/activate

```

``` bash

```