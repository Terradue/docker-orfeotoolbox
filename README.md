# opt-calibration - Optical calibration

Optical calibration

## Development 

```bash
cd opt_calibration
```

```bash
conda env create -f environment.yml
```

Activate the conda environment

```bash
conda activate  env_opt_calibration
```

To build and install the project locally:

```
python setup.py install
```

Test the CLI with:

```bash
opt-calibration --help
```

## Building the docker image

Build the docker image with:

```bash
docker build -t opt_calibration:0.1  -f .docker/Dockerfile .
```

or for pushing to the `terradue` docker repository:

```bash
docker build -t terradue/opt_calibration:0.1  -f .docker/Dockerfile .
```

Test the CLI with:

```bash
docker run --rm -it opt_calibration:0.1 opt-calibration --help
```

or 

```bash
docker run --rm -it terradue/opt_calibration:0.1 opt-calibration --help
```

## Creating the CWL

Check the examples provided in the `cwl-examples` folder and adapt one to the application requirements

## Setting up the git repository

```bash
git init
git remote add origin <git repository URL>
```

Once you're ready to add, commit and push, do:

```bash
git add -A
git commit -m 'first commit'
git push -u origin master
```
