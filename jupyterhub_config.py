import os
import sys
import shutil

c = get_config()

# Generic configuration
c.JupyterHub.admin_access = True
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True

# Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.SwarmSpawner'

# network configuration
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }

# List of available docker images
c.DockerSpawner.image_whitelist = {
    'Jupyter: Tensorflow': 'jupyter/tensorflow-notebook',
    'Jupyter: Data Science': 'jupyter/datascience-notebook',
    'Jupyter: Local Spark': 'jupyter/all-spark-notebook',
    'Jupyter: Scipy': 'jupyter/scipy-notebook',
    'Jupyter: R': 'jupyter/r-notebook',
    'Levell DataLab Python': os.environ['DOCKER_JUPYTER_CONTAINER']
}

# bindng address of jupyterhub
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_bind_url = 'http://0.0.0.0:8081'

c.DummyAuthenticator.password = "some_password"

# user data persistence
#c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
def create_dir_hook(spawner):
    username = spawner.user.name # get the username
    username = username.replace("@", "-40")
    username = username.replace(".", "-2e")
    
    volume_path = os.path.join('/srv/jupyterhub/data', username) #path on the jupytherhub host, create a folder based on username if not exists

    if not os.path.exists(volume_path):
        os.mkdir(volume_path)
        
        shutil.chown(volume_path, user='root', group='users')
        os.chmod(volume_path, 0o775)

c.Spawner.pre_spawn_hook = create_dir_hook

notebook_mount_dir = '/srv/docker/jupyter/{username}'
notebook_dir = '/home/jovyan/notebooks'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {notebook_mount_dir: {"bind": notebook_dir, "mode": "rw"}}

# Services
# timeout set to 24h = 3600s * 24h
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [
            sys.executable,
            '-m', 'jupyterhub_idle_culler',
            '--timeout=86400'
        ],
    }
]
