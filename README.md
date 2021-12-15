# About jupyter   
[![Publish levell jupyter docker image](https://github.com/jimmylevell/Jupyter/actions/workflows/action.yml/badge.svg?branch=master)](https://github.com/jimmylevell/Jupyter/actions/workflows/action.yml)  

levell jupyterhub container definition.    

## Frameworks used
- Jupyterhub
- Jupyter  
- scipy  

# Docker image details 
## Jupyterhub
Base image: jupyterhub/jupyterhub  
Exposed ports: 8000  
Additional installed resources:  
- Troubleshooting: vim, net-tools, dos2unix  
- Python libraries: dockerspawner, oauthenticator, jupyterhub-idle-culler

## Jupyter notebook
Base image: jupyter/scipy-notebook:33add21fab64         # special version for jupyterhub (https://github.com/jupyter/docker-stacks)  
Exposed ports: 8888  
Additional installed resources:  
- Troubleshooting: vim, net-tools, dos2unix  
- Data science: sklearn, pandas, seaborn

## Config
The service configuration can be done in the jupyterhub_config.py which is copied into the docker container at build time.  

For the authentication the auth0 client secret has to be stored in as docker secret:  
```
printf "clientsecret_auth0" | docker secret create auth0_jupyterhub_client_secret -
```

# Deployment
## General
Service: jupyter  
Data Path: /home/worker/levell/jupyter/  
Access URL: jupyter.app.levell.ch  

## Attached Networks
- traefik-public - access to reverse proxy
- levell_jupyter - attachable overlay network used by the spawned jupyter notebook containers

```
docker network create --driver=overlay levell_jupyter --attachable
```

## Attached volumes
jupyterdata: storing the jupyter notebooks, for each user a sub directory is created.  

## Environment variables 
DOCKER_JUPYTER_CONTAINER: jupyter/scipy-notebook:33add21fab64       # image the spawned containers are based on
DOCKER_NETWORK_NAME: levell_jupyter                                   # name of the network used for the spawned containers
CLIENT_SECRET: /run/secrets/auth0_jupyterhub_client_secret          # path to docker secret of the auth0 client secret
HUB_IP: 0.0.0.0             # binding IP address of the jupyterhub

# Authentication
Auth0
