<h1 align="center">
  <img src="../image/k8s-logo.png" alt="Kubernetes" width=120px height=120px >
  <br>
  Kubernetes - Parte 2
</h1>

<div align="center">

[![Status](https://img.shields.io/badge/version-1.0-blue)]()
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

# ReplicaSet
Quando um pod falha outro pod é criado para substituir o pod que falhou. 

# Deployment
Funciona como o replicaset

# Comandos

| **Comandos** | **Descrição** |
|----------|---------------|
| kubectl annotate deployment < nome do deployment > kubernetes.io/change-cause="Minha anotaçao" | Cria uma anotação no revision do **rollout**|
| kubectl get replicasets | Mostra  os replicasets |
| kubectl rollout history deployment < nome do deployment > | Mostra a versão do deployment |
| kubectl rollout undo deployment < nome do deployment > --to-revision=2 | Vouta para a versão 2 |


# Comando de Configurações
| **Comandos** | **Descrição** |
|----------|---------------|
| cat ~/.kube/config | Mostra as configurações |
| kubectl config view| Mostra as configurações do cluster do name space default |

