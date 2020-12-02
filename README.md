# Orfeo ToolBox (OTB) docker container

## Build

```console
docker build -f .docker/Dockerfile -t otb-7.2.0
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
