# Kubernetes Deployment - Flask App

Deploys the Flask app (built in Project 3) onto a Kubernetes cluster with
self-healing, load balancing, and auto-scaling — using Docker Desktop's
built-in Kubernetes.

## Project Structure
```
k8s_deployment/
├── namespace.yaml           # Isolated namespace for this app
├── deployment-local.yaml     # 3 replica pods running the local image
├── service.yaml              # LoadBalancer to expose the app
└── hpa.yaml                  # Auto-scales pods 2-6 based on CPU load
```

## Prerequisites
- Docker Desktop with Kubernetes enabled (Settings → Kubernetes → Enable Kubernetes)
- The app image built locally: `docker build -t flask-app:local .` (run in the Project 3 folder)

## Deploy

```bash
kubectl apply -f namespace.yaml
kubectl apply -f deployment-local.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
```

## Verify

```bash
kubectl get pods -n flask-app-ns
kubectl get service flask-app-service -n flask-app-ns
kubectl get hpa -n flask-app-ns
```

## Access the App

```bash
kubectl port-forward service/flask-app-service -n flask-app-ns 8080:80
```
Then open: `http://localhost:8080`

## Cleanup

```bash
kubectl delete namespace flask-app-ns
```

## Key Concepts Demonstrated
- **Deployment**: 3 replica pods with self-healing (auto-restart on crash)
- **Service (LoadBalancer)**: distributes traffic across pods
- **Namespace**: isolates this app's resources
- **HorizontalPodAutoscaler**: scales pods 2-6 based on real-time CPU usage
- **Liveness/Readiness Probes**: only routes traffic to healthy pods
- **Local image deployment**: uses `imagePullPolicy: Never` to run a locally
  built image without needing a container registry

## Connection to Project 3
The image (`flask-app:local`) is the same Flask app containerized in
Project 3 — this project takes that container and runs it as a managed,
scalable cluster instead of a single Docker container.
