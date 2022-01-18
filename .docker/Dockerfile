FROM centos:7


LABEL maintainer="Terradue S.r.l"
USER root

## yum
ADD .docker/install-yum.bash /tmp/install-yum.bash
ADD .docker/yum.list /tmp/yum.list
RUN set -x && chmod 755 /tmp/install-yum.bash && /tmp/install-yum.bash

ENV NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100 \
    SHELL=bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    CONDA_DIR=/opt/anaconda \
    NB_PYTHON_PREFIX=/opt/anaconda/envs/env_otb
    
ENV USER=${NB_USER} \
    NB_UID=${NB_UID} \
    HOME=/home/${NB_USER} 

ADD .docker/fix-permissions /usr/local/bin/fix-permissions

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    chmod g+w /etc/passwd /etc/group && \
    fix-permissions $HOME

# conda installation via miniforge
ADD .docker/install-miniforge.bash /tmp/install-miniforge.bash

ADD environment.yml /tmp/environment.yml

RUN chmod 755 /tmp/install-miniforge.bash && /tmp/install-miniforge.bash

ENV PATH=$NB_PYTHON_PREFIX/bin:$CONDA_DIR/bin:$PATH

# clean-up
RUN rm -f /tmp/install-*.bash && rm -f /tmp/environment.yml 

# fix permissions
RUN chown -R $NB_USER:$NB_GID ${HOME} 

USER ${NB_USER}

# workdir for binder
COPY --chown=${NB_USER}:${NB_GID} . ${HOME}

ENV PREFIX ${NB_PYTHON_PREFIX}

ENV PATH ${NB_PYTHON_PREFIX}/bin:$PATH

ENV CMAKE_PREFIX_PATH=${NB_PYTHON_PREFIX}/conda-otb \
    PYTHONPATH=${NB_PYTHON_PREFIX}/conda-otb/lib/python \
    GDAL_DATA=${NB_PYTHON_PREFIX}/conda-otb/share/gdal \
    PROJ_LIB=${NB_PYTHON_PREFIX}/conda-otb/share/proj \
    LC_NUMERIC=C \
    OTB_APPLICATION_PATH=${NB_PYTHON_PREFIX}/conda-otb/lib/otb/applications \
    LD_LIBRARY_PATH=/opt/anaconda/envs/env_opt_calibration/lib \
    PATH=${NB_PYTHON_PREFIX}/conda-otb/bin:$PATH

WORKDIR ${HOME}
