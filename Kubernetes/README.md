# Health-Analysis
__Deployed at GCP GKE__  
The main objectie of the project was to:  
1. Create a Docker image for dash app for which python:3.8.5 was used  
``` bash
git clone https://github.com/kshitijmamgain/Health-Analysis
cd Health-Analysis/Kubernetes
docker build -t health-app:v1 .
docker images
```
2. Test the container created from Docker image locally by binding the port in GCloud editor with 
``` bash
docker run -p 8080:8080 --name my-app health-app:v1 
```
Doing this would allow us to preview tha app in GCloud on local host 8080  
3. Push the Docker image to Google Container Registry
``` bash
docker tag health-app:v1 gcr.io/my-project/halth-app:v1
```
_Note_: gcr.io api should be enabled and is also billed, documentation for doing that is plentifully available.  
4. Now since the image was succesfully created and tested, we use it to create and expose deployment in Kubernetes. I created kubernetes cluster with 2 nodes.   
```bash 
kubectl create cluster health-app --num-node=2
```
_Note_: It took me a lot of time to debug my next actionsm beacuse we have to get the credentials for GKE cluster
```bash
gcloud container clusters get-credentials health-app
```
Then, I created deployment.yaml file and did following:
``` bash
# create deployment
kubectl apply -f deployment.yaml
# view running deployment
kubectl get deployments
# create load balancer to view the app
kubectl expose deployment health-app --type=LoadBalancer --port 80 --target-port 8080
# get ip address
kubectl get services
```
The app was then available on external ip address.  
5. I updated my deployment by pushing new image after editing deployment
```bash
kubectl edit deployment health-app
```
Which opens the deployment and we could make changes. I changed the replica and image tag to test which worked well.  
5. The last step was to create CI/CD pipeline using Jenkins. I would explain this step in detail in my blog.
