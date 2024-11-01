# LocalDymension

### Use the state export in LocalDymension

1. Ensure you have state export with filename `export.json``


2. Ensure you have docker and docker-compose installed:

```sh
# Docker
sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
sudo apt install docker.io -y

# Docker compose
sudo apt install docker-compose -y
```

3. Init chain

```sh
bash init.sh
```

4. Clone Dymension Hub repository then checkout the commit you want and run the build image command:

```sh
docker build -t ghcr.io/dymensionxyz/dymension:local -f Dockerfile .
```

5. Run 4 validators node

```sh
docker-compose up
```
