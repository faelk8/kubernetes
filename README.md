# Versão 1
# Iniciando o cluster Kubernetes 

Arquivo kind com o código para a criação do cluster.

kind.yaml
```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4

nodes:
- role: control-plane # Gerenciador
- role: worker
- role: worker
- role: worker
```
Comando para criar o kluster:

```
kind create cluster --config=k8s/kind.yaml --name=meu-cluster
```

Verificar o status do cluster
```
kind cluster-info --context kind-meu-cluster
```

# Criando o servidor web em Go
1.0
server.go
```
package main

import "net/http"

func main() {
	http.HandleFunc("/", Hello)
	http.ListenAndServe(":80", nil)

}

func Hello(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("<h1>Rafael Batista</h1>"))
}

```
go.mod sem esse arquivo não funciona
```
module server.go

go 1.18
```

# Construindo a Imagem 
Build da imagem e push

```
docker build -t faelk8/hello-go . && docker push faelk8/hello-go:v1

```

Executar o container
```
docker run --rm -p 8080:8080 faelk8/hello-go

```

# Pod
Menor objeto do Kubernetes, o container roda dentro do pod.
pod.yaml
```
apiVersion: v1
kind: Pod
metadata:
  name: "goserver"
  labels:
    name: "pyserver"
spec:
  containers:
  - name: goserver
    image: "faelk8/hello-go:v1"
```

Criando o pod

```
kubectl apply -f k8s/pod.yaml
```

Liberando uma porta para conexão 
```
kubectl port-forward pod/goserver 8080:8080
```
Para acessar  http://localhost:8080

# Replica Set
Cria replicas de pod, quando um pod cai o replicaset cria outro pod. Vai sempre manter a quantidade de pods ativos de acordo com o valor de replicas informado.
```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: goserver
  labels:
    app: goserver
spec:
  replicas: 3
  selector:
    matchLabels:
      app: goserver
  template:
    metadata:
      labels:
        app: goserver
    spec:
      containers:
        - name: goserver
          image: faelk8/hello-go:v1
```
Comando para criar o replicaset
```
kubectl apply -f k8s/replicaset.yaml
```
> [!WARNING]  
> Quando atualizar o código do replicaset e fazer um novo apply as mudanças não são aplicadas, para funcionar precisa deletar todos os pods para que sejam recriados com a nova versão.

# Deployment

Deployment cria o replicaset que cria o pod.
Quando muda a versão do deployment ele derruba tudo e cria com a nova versão.

Para criar um deployment basta mudar o valo do kind.
```
kind: Deployment
```

# Rollout
Quando a versão atual apresenta algum problema e precisa voltar para a versão anterior.

Comando para ver as versões.
```
kubectl rollout history deployment goserser
```

Comando para voltar a última versão.
```
kubectl rollout undo deploymente goserver
```

Para voltar para uma versão específica informando o número da versão.
```
kubectl rollout undo deployment goserver --to-revision=1
```

# Comandos

| **Comandos** | **Descrição** |
|----------|---------------|
| kubectl apply -f k8s/pod.yaml | Cria um pod					| 
| kubectl apply -f k8s/replicaset.yaml | Cria um pod com replicas| 
| kubectl apply -f k8s/deploymente.yaml | Cria o replicaset que cria o pod| 
| kubectl delete goserver		| Delete o pod com o nome goserver | 
| kubectl delete replicaset goserver | Deleta o replicaset com o nome goserver
| kubectl get nodes 		    | Mostra os nodes  				|
| kubectl get replicaset 				| Mostra como está replicado|
| kubectl get po 			    | Mostra os pods				|
| kubectl get pods 				| Mostra os pods 				|
