# Orfeo ToolBox (OTB) docker container

## Get the docker 

```console
docker pull terradue/otb-7.2.0
```

Run a container: 

```console
docker run --rm -it terradue/otb-7.2.0:latest bash
```

## Run

Bash console

```console
docker run --rm -it otb-7.2.0:latest bash
```

OTB cli applications are available in PATH.

Python 

```console
docker run --rm -it otb-7.2.0:latest bash
```

then

```console
python
```

```python
import otbApplication
import gdal
```

## Extend the conda environment

```console
conda install -n env_otb <some package>
```

## Build

Clone this repo and: 

```console
docker build -f .docker/Dockerfile -t otb-7.2.0
```