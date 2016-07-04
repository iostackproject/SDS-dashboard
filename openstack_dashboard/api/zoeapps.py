#IBM NOTEBOOK SECTION
#spark master & worker

NB_APP_NAME = 'ibm-notebook'
SPARK_MASTER_MEMORY_LIMIT = 512 * (1024 ** 2)  # 512MB
SPARK_WORKER_MEMORY_LIMIT = 12 * (1024 ** 3)  # 12GB
NOTEBOOK_MEMORY_LIMIT = 4 * (1024 ** 3)  # 4GB, contains also the Spark client
SPARK_WORKER_CORES = 6
SPARK_WORKER_COUNT = 2
DOCKER_REGISTRY = '172.17.131.201:5000'  # Set to None to use images from the Docker Hub
SPARK_MASTER_IMAGE = 'iostackrepo/spark-master-ibm'
SPARK_WORKER_IMAGE = 'iostackrepo/spark-worker-ibm'
NOTEBOOK_IMAGE = 'iostackrepo/spark-jupyter-notebook-ibm'

MPI_APP_NAME = 'openmpi-dyna'
WORKER_MEMORY = 5 * (1024 ** 3)  # configurabile
WORKER_COUNT = 4
CPU_COUNT_PER_WORKER = 1
MPIRUN_IMAGE = 'iostackrepo/openmpi-centos5'
WORKER_IMAGE = 'iostackrepo/openmpi-centos5'
MPIRUN_COMMANDLINE = 'mpirun --mca oob_tcp_if_include eth0 --mca btl_tcp_if_include eth0 -x LSTC_LICENSE_SERVER_PORT -x LSTC_LICENSE_SERVER -x LSTC_LICENSE -hostfile hostlist -wdir /mnt/workspace /mnt/workspace/ls-dyna_mpp_s_r7_1_2_95028_x64_redhat54_ifort131_sse2_openmpi165 i=Combine.key memory=1024m memory2=512m 32ieee=yes nowait'
ENV = [
    ["LSTC_LICENSE", "network"],
    ["LSTC_LICENSE_SERVER", "10.30.1.7"],
    ["LSTC_LICENSE_SERVER_PORT", "31010"]
]

def spark_master_service(mem_limit, image):
    """
    :type mem_limit: int
    :type image: str
    :rtype: dict
    """
    service = {
        'name': "spark-master",
        'docker_image': image,
        'monitor': False,
        'required_resources': {"memory": mem_limit},
        'ports': [
            {
                'name': "Spark master web interface",
                'protocol': "http",
                'port_number': 8080,
                'path': "/",
                'is_main_endpoint': False
            }
        ],
        'environment': [
            ["SPARK_MASTER_IP", "spark-master-0-{execution_name}-{user_name}-{deployment_name}-zoe.{user_name}-{deployment_name}-zoe"],
            ["HADOOP_USER_NAME", "{user_name}"]
        ],
        'networks': [],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    return service


def spark_worker_service(count, mem_limit, cores, image):
    """
    :type count: int
    :type mem_limit: int
    :type cores: int
    :type image: str
    :rtype List(dict)
    :param count: number of workers
    :param mem_limit: hard memory limit for workers
    :param cores: number of cores this worker should use
    :param image: name of the Docker image
    :return: a list of service entries
    """
    worker_ram = mem_limit - (1024 ** 3) - (512 * 1025 ** 2)
    service = {
        'name': "spark-worker",
        'docker_image': image,
        'monitor': False,
        'required_resources': {"memory": mem_limit},
        'ports': [
            {
                'name': "Spark worker web interface",
                'protocol': "http",
                'port_number': 8081,
                'path': "/",
                'is_main_endpoint': False
            }
        ],
        'environment': [
            ["SPARK_WORKER_CORES", str(cores)],
            ["SPARK_WORKER_RAM", str(worker_ram)],
            ["SPARK_MASTER_IP", "spark-master-0-{execution_name}-{user_name}-{deployment_name}-zoe.{user_name}-{deployment_name}-zoe"],
            ["SPARK_LOCAL_IP", "spark-worker-{index}-{execution_name}-{user_name}-{deployment_name}-zoe.{user_name}-{deployment_name}-zoe"],
            ["HADOOP_USER_NAME", "{user_name}"]
        ],
        'networks': [],
        'total_count': count,
        'essential_count': 1,
        'startup_order': 1
    }
    return service


#spark-jupyter
def spark_jupyter_notebook_service(mem_limit, worker_mem_limit, image):
    """
    :type mem_limit: int
    :type worker_mem_limit: int
    :type image: str
    :rtype: dict
    """
    executor_ram = worker_mem_limit - (1024 ** 3) - (512 * 1025 ** 2)
    driver_ram = (2 * 1024 ** 3)
    service = {
        'name': "spark-jupyter",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": mem_limit},
        'ports': [
            {
                'name': "Spark application web interface",
                'protocol': "http",
                'port_number': 4040,
                'path': "/",
                'is_main_endpoint': False
            },
            {
                'name': "Jupyter Notebook interface",
                'protocol': "http",
                'port_number': 8888,
                'path': "/",
                'is_main_endpoint': True,
                'expose': True
            }
        ],
        'environment': [
            ["SPARK_MASTER", "spark://spark-master-0-{execution_name}-{user_name}-{deployment_name}-zoe.{user_name}-{deployment_name}-zoe:7077"],
            ["SPARK_EXECUTOR_RAM", str(executor_ram)],
            ["SPARK_DRIVER_RAM", str(driver_ram)],
            ["HADOOP_USER_NAME", "{user_name}"],
            ["NB_USER", "{user_name}"]
        ],
        'networks': [],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    return service

#notebook
def spark_jupyter_notebook_ibm_app(name,
                                   notebook_mem_limit, master_mem_limit, worker_mem_limit, worker_cores,
                                   worker_count,
                                   master_image, worker_image, notebook_image):
    sp_master = spark_master_service(int(master_mem_limit), master_image)
    sp_workers = spark_worker_service(int(worker_count), int(worker_mem_limit), int(worker_cores), worker_image)
    jupyter = spark_jupyter_notebook_service(int(notebook_mem_limit), int(worker_mem_limit), notebook_image)

    app = {
        'name': name,
        'version': 2,
        'will_end': False,
        'priority': 512,
        'requires_binary': False,
        'services': [
                        sp_master,
                        sp_workers,
                        jupyter,
                    ]
    }
    return app


def create_notebook_app(app_name=NB_APP_NAME, notebook_memory_limit=NOTEBOOK_MEMORY_LIMIT,
               spark_master_memory_limit=SPARK_MASTER_MEMORY_LIMIT, spark_worker_memory_limit=SPARK_WORKER_MEMORY_LIMIT,
               spark_worker_cores=SPARK_WORKER_CORES, spark_worker_count=SPARK_WORKER_COUNT,
               docker_registry=DOCKER_REGISTRY, spark_master_image=SPARK_MASTER_IMAGE,
               spark_worker_image=SPARK_WORKER_IMAGE, notebook_image=NOTEBOOK_IMAGE):
    if docker_registry is not None:
        spark_master_image = docker_registry + '/' + spark_master_image
        spark_worker_image = docker_registry + '/' + spark_worker_image
        notebook_image = docker_registry + '/' + notebook_image

    return spark_jupyter_notebook_ibm_app(app_name, notebook_memory_limit, spark_master_memory_limit,
                                          spark_worker_memory_limit, spark_worker_cores, spark_worker_count,
                                          spark_master_image, spark_worker_image, notebook_image)


#idiada
def openmpi_worker_service(count, image, worker_memory):
    """
    :type counter: int
    :type worker_memory: int
    :rtype: dict
    """
    service = {
        'name': "mpiworker",
        'docker_image': image,
        'monitor': False,
        'required_resources': {"memory": worker_memory},
        'ports': [],
        'environment': [],
        'volumes': [],
        'command': '',
        'total_count': count,
        'essential_count': count,
        'startup_order': 0
    }
    return service


def openmpi_mpirun_service(mpirun_commandline, image, worker_memory):
    """
    :type mpirun_commandline: str
    :type worker_memory: int
    :rtype: dict
    """
    service = {
        'name': "mpirun",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": worker_memory},
        'ports': [],
        'environment': [],
        'volumes': [],
        'command': mpirun_commandline,
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 1
    }
    return service



def openmpi_app(name, mpirun_image, worker_image, mpirun_commandline, worker_count, worker_memory):
    app = {
        'name': name,
        'version': 2,
        'will_end': True,
        'priority': 512,
        'requires_binary': True,
        'services': []
    }
    proc = openmpi_worker_service(worker_count, worker_image, worker_memory)
    proc['environment'] += ENV
    app['services'].append(proc)
    proc = openmpi_mpirun_service(mpirun_commandline, mpirun_image, worker_memory)
    proc['environment'] += ENV
    app['services'].append(proc)
    return app


def create_idiada_app(app_name=MPI_APP_NAME, mpirun_image=MPIRUN_IMAGE, worker_image=WORKER_IMAGE,
               mpi_commandline=MPIRUN_COMMANDLINE, worker_count=WORKER_COUNT, worker_memory=WORKER_MEMORY,
               docker_registry=DOCKER_REGISTRY, cpu_count_per_worker=CPU_COUNT_PER_WORKER):
    if docker_registry is not None:
        mpirun_image = docker_registry + '/' + mpirun_image
        worker_image = docker_registry + '/' + worker_image

    with open('hostlist', 'w') as fp:
        for wc in range(worker_count):
            fp.write(
                'mpiworker{}-mpidynademo-zoeadmin-iostack-zoe slots={} max-slots={}\n'.format(wc, cpu_count_per_worker,
                                                                                              cpu_count_per_worker))
    print('Wrote MPI host list file in "hostlist", execution name set to "mpidynademo"')
    return openmpi_app(app_name, mpirun_image, worker_image, mpi_commandline, worker_count, worker_memory)


