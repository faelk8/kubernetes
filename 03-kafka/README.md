<h1 align="center">
  <img src="../image/k8s-logo.png" alt="Kubernetes" width=120px height=120px >
  <img src="../image/kafka.png" alt="Kubernetes" width=120px height=120px >
  <br>
  Kubernetes Kafka
</h1>

<div align="center">

[![Status](https://img.shields.io/badge/version-0.1-blue)]()
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>




Não precisa de um .yaml

Aplica a alteração
```
kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-persistent-single.yaml -n kafka
```

Para assistir
```
kubectl get pods -n kafka -w
```
Sem assistir
```
kubectl get pods -n kafka
```
<hr>
<hr>
<hr>

kind create cluster  --name=kafka

Name space
kubectl create ns kafka