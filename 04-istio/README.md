<h1 align="center">
  <img src="../image/istio.png" alt="Kubernetes" width=400px height=250px >
  <br>
  Kubernetes - Istio
</h1>

<div align="center">

[![Status](https://img.shields.io/badge/version-1.0-blue)]()
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

# Iniciando o cluster
```
k3d cluster create -p "8000:30000@loadbalancer" --agents 2
# trocando de contexto
kubectl config use-context k3d-k3s-default
```
Para ver se o serviço está rodando:
```
kubectl get po -n istio-system
```

# Instalando o Proxy
```
kubectl label namespace default istio-injection=enable
```
`deployment.yaml`
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
        ports:
        - containerPort: 80
```

# Observabilidade

```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
```
Abrindo o dashboard
```
istioctl dashboard kiali
```