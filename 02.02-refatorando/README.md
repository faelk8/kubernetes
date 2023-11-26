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

# Persistência de Dados
A persistência de dados refere-se à capacidade de manter a integridade e a disponibilidade dos dados além da execução temporária de um programa ou processo. Em sistemas de computação, a persistência de dados é fundamental para garantir que as informações não se percam quando um programa é encerrado, um sistema é reiniciado ou um dispositivo é desligado.

## Volumes
Os Volumes no Kubernetes são meios eficazes para lidar com o armazenamento de dados associados a contêineres em Pods. Eles possuem um ciclo de vida que está diretamente ligado ao ciclo de vida do Pod em que estão inseridos. Vale destacar que, mesmo em caso de falha do Pod, os dados armazenados no Volume permanecem preservados. Contudo, é importante notar que a associação específica entre o Pod e o Volume é perdida em caso de falha.

## Persistents Volumes
Solução robusta para o armazenamento de dados no Kubernetes. Eles têm ciclos de vida independentes dos Pods, o que significa que persistem mesmo quando os Pods são reiniciados ou removidos. Para acessar um Volume Persistente, é necessário criar um PersistentVolumeClaim, que atua como uma solicitação para obter acesso a uma porção específica do Volume Persistente.

## Persistent Volume Claim
tua como uma espécie de pedido formal por uma quantidade específica de armazenamento em um PersistentVolume. Quando um PersistentVolumeClaim é criado, o Kubernetes tenta vinculá-lo a um PersistentVolume disponível que atenda aos requisitos da solicitação. Isso proporciona uma camada adicional de abstração, permitindo que os desenvolvedores solicitem e acessem armazenamento persistente de maneira simplificada e eficiente.

## Storage Classes
Fornecem uma maneira flexível de definir as propriedades do armazenamento no Kubernetes. Elas permitem que os administradores de cluster forneçam perfis de armazenamento predefinidos para os desenvolvedores, simplificando a configuração e o provisionamento de armazenamento. Ao utilizar Storage Classes, é possível definir características como tipo de armazenamento, provisionamento dinâmico e políticas de reciclagem, proporcionando maior controle e eficiência na gestão do armazenamento


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

