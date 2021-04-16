# Serving DSVM trained TF Keras model to Kubernetes cluster using MLflow

In this article, you:

1. Train model with tensorflow keras, save the trained model with mlflow.keras.save_model() api
2. Build docker image with mlflow command line
3. Push the docker image to Azure Container Registry
4. Deploy the docker image to Azure Stack Hub hosted Kubernetes
5. Test the deployment.

## Prerequisites
1. [Data Science Virtual Machine- Ubuntu 18.04](https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/dsvm-ubuntu-intro)

   Please make sure to select "Password" for Authentication type,  as JupyterHub is not configured to use SSH public keys.
   
2. MLFlow is installed to your conda virtual environment.

```
conda activate myenv

pip install mlflow

```

For more details about installing packages to your conda environment, please see [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html)

3. [Docker is installed](https://docs.docker.com/engine/install/ubuntu/).

4. [Azure Container Registry is installed](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal) 
   and [Authencated with Service principal](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication)
   
5. A Kubernetes cluster. You can choose one hosted in you Azure Stack Hub.

## Train a Tensorflow Keras model and save the trained model with mlflow.keras.save_model() api with JupyterHub.

Please see the [sample notebook](notebooks/image_classification_mnist_tf_mlflow-no-run.ipynb)

## Build docker image with MLflow

```
    mlflow models build-docker -m <model_folder>  -n  <image_name>
```
Here <model_folder> is the folder where model artifacts are saved. it should contain a MLmodel file, conda.yaml and data folder.


## Push image to azure container registry

1.  docker login to ACR:
       
``` docker login myregistry.azurecr.io --username $SP_APP_ID --password $SP_PASSWD ```
       
2.  use "docker image tag" to tag your image into format as
       
``` docker image tag pfmnist-keras  slash2acr.azurecr.io/mlflow/pfmnist-keras ```

3.  push the image to Azure Container Registry
    
``` docker push slash2acr.azurecr.io/mlflow/pfmnist-keras ```
       
       
##  Use kubectl to deploy the image and expose the pod through loadbalancer resources of kubernetes.

1. [Create a Kubernetes secret](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-auth-kubernetes)
      
      ```
      kubectl create secret docker-registry <secret-name> \
    --namespace <namespace> \
    --docker-server=<container-registry-name>.azurecr.io \
    --docker-username=<service-principal-ID> \
    --docker-password=<service-principal-password>
    
      ```
    
2. Use following deploy.yaml file to deploy:

```
kubectl apply -f yaml/mnist_deploy_acr.yml

```

3.  Retrieve External IP address of the svc created in deployment:

``` kubectl get svc mnist-acr ```

## Test the service

The inference url is "http://<external_ip>/invocations". Here we included a sample input at notebooks/sample_input_keras.json.
You may use postman to test it. The output is something like:

```
[
  [
    -6.065847873687744,
    -7.9559006690979,
    13.702223777770996,
    1.1550079584121704,
    -3.750947952270508,
    -3.2751076221466064,
    -3.2166898250579834,
    -4.364444732666016,
    -0.2577851414680481,
    -3.623817205429077
  ]
]
```

       

