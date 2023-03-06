###############################################################################################
# levell jupyter hub - BASE
###############################################################################################
FROM jupyterhub/jupyterhub:3.1.1 as levell-jupyterhub-base

RUN mkdir -p /srv/jupyterhub
WORKDIR /srv/jupyterhub

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update
RUN apt-get upgrade -y
RUN apt-get install vim -y
RUN apt-get install net-tools -y
RUN apt-get install dos2unix -y

###############################################################################################
# levell jupyter - PRODUCTION
###############################################################################################
FROM levell-jupyterhub-base as levell-jupyterhub-deploy

COPY jupyterhub_config.py .

# Install dependencies (for advanced authentication and spawning)
RUN pip install \
    dockerspawner \
    jupyterhub-idle-culler

###############################################################################################
# levell jupyter - BASE
###############################################################################################
FROM jupyter/scipy-notebook:2023-03-06 as levell-jupyternotebook-base

WORKDIR /var/www

USER root

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update
RUN apt-get upgrade -y
RUN apt-get install vim -y
RUN apt-get install net-tools -y
RUN apt-get install dos2unix -y

USER jovyan

###############################################################################################
# levell jupyter - PRODUCTION
###############################################################################################
FROM levell-jupyternotebook-base as levell-jupyternotebook-deploy

# install pip applications
RUN pip install --upgrade pip
RUN pip install sklearn
RUN pip install pandas
RUN pip install seaborn
