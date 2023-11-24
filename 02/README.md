<h1 align="center">
  <img src="../image/k8s-logo.png" alt="Kubernetes" width=120px height=120px >
  <br>
  Kubernetes - Gerenciando um Server em Go
</h1>

<div align="center">

[![Status](https://img.shields.io/badge/version-1.0-blue)]()
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

# Kubernetes

O Kubernetes é uma plataforma de código aberto para automatizar a implantação, escalonamento e operação de aplicativos em contêineres. Ele utiliza uma arquitetura mestre/nó para gerenciar e orquestrar os contêineres de maneira eficiente.

## Mestre (Master)
O componente mestre é o cérebro do cluster Kubernetes, responsável por gerenciar e manter o estado desejado do sistema. Ele consiste em:
- **API Server:** Uma interface REST que recebe e executa comandos para interagir com o cluster. Os administradores e usuários utilizam essa API para controlar o ambiente.
- **Controller Manager:** Responsável por garantir que o estado atual do sistema corresponda ao estado desejado. Isso inclui o Controller Manager que gerencia objetos como ReplicaSets e Deployments.
- **Scheduler:** Encarregado de decidir onde os pods (a menor unidade em Kubernetes) serão executados no cluster, levando em consideração os recursos disponíveis e as políticas definidas.
- **ETCD:** Um banco de dados chave-valor altamente disponível que armazena todos os dados vitais do cluster. Ele serve como o cérebro persistente do Kubernetes, mantendo o estado do sistema mesmo após falhas.

## Nó (Node)
Os nós são as máquinas físicas ou virtuais que compõem o cluster. Eles executam as aplicações empacotadas em contêineres. Cada nó possui:
- **Kubelet:** Agente que executa na máquina e garante que os containers estejam em execução nos pods.
- **KubeProxy:** Facilita a comunicação entre os pods e gerencia as regras de rede. É responsável por garantir que os pods possam se comunicar entre si, mesmo que estejam em diferentes nós.

## API
O Kubernetes fornece uma variedade de objetos que podem ser gerenciados por meio da API. Alguns desses objetos incluem:
- **Pod:** A menor unidade em Kubernetes, representando um único processo em execução em algum lugar no cluster.
- **ReplicaSet:** Mantém um conjunto especificado de réplicas de pods em execução para garantir a disponibilidade e escalabilidade.
- **Deployment:** Define como os pods são implantados e atualizados. Facilita a atualização e rotação de novas versões de aplicações.
- **Volume:** Um diretório acessível a containers em um pod. Pode ser usado para armazenamento durável ou para compartilhamento de dados entre pods.


# Iniciando o cluster Kubernetes 
Arquivo kind com o código para a criação do cluster.<br>
`kind.yaml`
```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4

nodes:
- role: control-plane
```
Comando para criar o kluster:
```
kind create cluster --config=k8s/kind.yaml --name=meu-cluster
```

Verificar o status do cluster
```
kind cluster-info --context kind-meu-cluster
```

# Criando um Pod
`pod.yaml`
```
apiVersion: v1
kind: Pod
metadata:
  name: pod-nginx
spec:
  containers:
    - name: container-nginx
      image: nginx:latest
```
Aplicando
```
kubectl apply -f k8s/pod.yaml
```

# Trabalhando com SVC
* Abstração para expor aplicaçãoes executando em um ou mais pods
* Provem IP's fixos para comunicação
* Provem um DNS para um ou mais pods
* São capazes de fazer balanceamento de carga


# Comandos

| **Comandos** | **Descrição** |
|----------|---------------|
| kubectl api-resources | Mostra  os recursos |
| kubectl apply -f < nome > | Para aplicar o arquivo |
| kubectl delete pod < nome > | Delete o pod |
| kubectl describe pod < nome > | Mostra as informaçoes |
| kubectl exec -it < nome do pod > -- bash | Entra no modo interativo |
| kubectl get po | Mostra os pods ativos |
| kubectl get pods --watch | Acompanhar os pods |
| kubectl get po -o wide | Mostra mais informações |


# Comando de Configurações
| **Comandos** | **Descrição** |
|----------|---------------|
| cat ~/.kube/config | Mostra as configurações |
| kubectl config view| Mostra as configurações do cluster do name space default |