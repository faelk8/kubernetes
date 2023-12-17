<h1 align="center">
  <img src="../image/istio.png" alt="Kubernetes" width=400px height=250px >
  <br>
  Kubernetes - Gerenciando um Server em Go
</h1>

<div align="center">

[![Status](https://img.shields.io/badge/version-1.0-blue)]()
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

# Iniciando o cluster
```
k3d cluster create -p "8000:30000@loadbalancer" --agents 2
```