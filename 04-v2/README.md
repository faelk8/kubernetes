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
server.go
```
package main

import "net/http"

func main() {
	http.HandleFunc("/", Hello)
	http.ListenAndServe(":9000", nil)

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

replicaset.yaml
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

deployment.yaml
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

# Acessando o Services
Atua como um load balancer gerenciado pelo próprio Kubernetes.

**Cluster IP**

service.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: service-goserver
spec:
  selector:
    app: goserver
  type: ClusterIP
  ports:
  - name: goserver-service
    port: 9000
    protocol: TCP
```

**name: serivce-goserver =  host**

Comando para iniciar.
```
kubectl apply -f k8s/service.yaml
```

O service foi iniciado mas o acesso ainda precisa liberar a porta para acesso.
```
kubectl port-forward svc/service-goserver 9000:9000
```

**Target Port**

Redirecionamento de porta. Quando acessar a porta 9000 o service redireciona para a porta 5000 do container.

service.go
```
func main() {
	http.HandleFunc("/", Hello)
	http.ListenAndServe(":5000", nil)

}
```

Aplicar alteração.
```
kubectl apply -f k8s/service.yaml
```

Aplicar alteração.
```
kubectl apply -f k8s/service.yaml
```

Comando para acesso.
```
kubectl port-forward svc/service-goserver 9000:9000
```

service.yaml
```
  - name: goserver-service
    port: 9000
    targetPort: 5000
    protocol: TCP
```

**NodePort**

Quando tem várias nodes trabalhando e se tem um acesso por uma porta específica todos os nodes liberam o acesso para aquela vai entrar no serviço.

Utilizado para testes e serviços temporários.

service.yaml
```
  - name: goserver-service
    port: 9000
    protocol: TCP
    nodePort: 300001 #30.000 32.767
```

Aplicar alteração.
```
kubectl apply -f k8s/service.yaml
```

Comando para acesso.
```
kubectl port-forward svc/service-goserver 9000:9000
```

**Load Balancer**

Gera um IP para acessar a aplicação de fora, utiizando para nuvem. Gera um PORT.

service.yaml
```
  type: LoadBalancer
```
Aplicar alteração.
```
kubectl apply -f k8s/service.yaml
```

Comando para acesso.
```
kubectl port-forward svc/service-goserver 9000:9000
```



# Proxy 
Acessando a rede interna do Kubernetes 

Lista de todos os serviços.
```
kubectl proxy --port=8080
```


# Variáveis de Ambiente
Alterando o código go para incluir variáveis.

server.go
```
func Hello(w http.ResponseWriter, r *http.Request) {
	name := os.Getenv("NAME")
	age := os.Getenv("AGE")
	fmt.Fprintf(w, "Hello, I'm %s. I'm %s", name, age)
}
```

deployment.yaml
```
      containers:
        - name: goserver
          image: faelk8/hello-go:v1.1
          env: 
            - name: NAME 
              value: "Rafael"
            - name: AGE 
              value: "35"
```
Comandos para aplicar a atualização.
```
docker  build -t faelk8/hello-ho:v1.1 . && dockr push faelk8/hello-go:v1.1

kubeclt apply -f k8s/deployment.yaml
```
Acessando o serviço.
```
kubectl port-forward svc/service-goserver 9000:9000
```

# Config Map
Mapeando variáveis de ambiente.

Forma mais simples.
congigmap-env.yaml
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-goserver
data:
  NAME: "Rafael"
  AGE: "35"
```

Aplicando as alterações.
```
kubectl apply -f k8s/configmap-env.yaml
kubectl apply -f f8s/deployment.yaml
```
Acessando a aplicação.
```
kubectl port-forward svc/service-goserver 9000:9000
```

Arquivos que armazena as variáveis de ambiente.

deployment.yaml
```
      containers:
        - name: goserver
          image: faelk8/hello-go:v1.1
          env: 
            - name: NAME 
              valueFrom: 
                configMapKeyRef:
                  name: env-goserver
                  key: NAME
            - name: AGE 
              valueFrom: 
                configMapKeyRef:
                  name: env-goserver
                  key: AGE
```

Aplicando as alterações.
```
kubectl apply -f k8s/configmap-env.yaml
kubectl apply -f f8s/deployment.yaml
```
Acessando a aplicação.
```
kubectl port-forward svc/service-goserver 9000:9000
```

Forma mais avançada, carrega todas as variáveis de ambiente.
deployment.yaml
```
    spec:
      containers:
        - name: goserver
          image: faelk8/hello-go:v1.1
          envFrom:
            - configMapRef:
                name: env-goserver
```

Aplicando as alterações.
```
kubectl apply -f k8s/configmap-env.yaml
kubectl apply -f f8s/deployment.yaml
```
Acessando a aplicação.
```
kubectl port-forward svc/service-goserver 9000:9000
```


# Secret
Oculta o valor mas não protege. Usa o base64. Não é criptografia.

server.go
```
func main() {
	http.HandleFunc("/secret", Secret)
  ...
```
secret.yaml
```
apiVersion: v1
kind: Secret
metadata:
  name: secret-goserver
type: Opaque
data:
  USER: "cmFmYWVsCg=="
  PASSWORD: "MTIzNDU2NzgK"
```
base64
```
echo "rafael" | base64
echo "12345678" | base64
```
deployment.yaml
```
    spec:
      containers:
        - name: goserver
          image: faelk8/hello-go:v1.4
          envFrom:
            - configMapRef:
                name: env-goserver
            - secretRef:
                name: secret-goserver
```

Aplicar alteração:
```
docker build -t faelk8/hello-go:v1.4 . && docker push faelk8/hello-go:v1.4
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml

```
**Acessar:**  www.localhost:9090/secret

# Health Check
Verificar a saúde da aplicação. Até 25 segundos vai estar funcionando, depois vai apresentar erro, porém continua rodando.

**Liveness**
server.go
```
var startedAt = time.Now()

func main() {
	http.HandleFunc("/healthz", Healthz)
  ...

func Healthz(w http.ResponseWriter, r *http.Request) {
	duration := time.Since(startedAt)
	if duration.Seconds() > 25 {
		w.WriteHeader(500)
		w.Write([]byte(fmt.Sprintf("Duração: %v", duration.Seconds())))
	} else {
		w.WriteHeader(200)
		w.Write([]byte("ok"))

	}
}  
deployment.yaml
```
image: faelk8/hello-go:1.5
```

```
Aplicando a alteração.
```
docker build -t faelk8/hello-go:1.5 . && docker push faelk8/hello-go:1.5
kubectl apply -f k8s/deployment.yaml
Kubectl port-forward svc/service-goserver  9000:9000
```

**LivenessProbe**
3 formas.

```
      containers:
        - name: goserver
          image: faelk8/hello-go:1.5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 9000
            periodSeconds: 5
            failureThreshold: 3
            timeoutSeconds: 1
            successThreshold: 1
```

Aplicar alteração e assistir os pods.
```
kubectl apply -f k8s/deployment.yaml && watch -n1 kubectl get pods
```
**Readiness**

Verifica quando a aplicação está pronta.

server.go
```
  if duration.Seconds() < 10 {
    ...
```
deployment.yaml
```
image: faelk8/hello-go:1.5

          readinessProbe:
            httpGet:
              path: /healthz
              port: 9000
            periodSeconds: 3
            failureThreshold: 1
            timeoutSeconds: 1
            successThreshold: 1
            initialDelaySeconds: 10

# Comentar o liveness
```

Aplciar alteração.
```
docker build -t faelk8/hello-go:1.6 . && docker push faelk8/hello-go:1.6
kubectl apply -f k8s/deployment.yaml && watch -n1 kubectl get pods
```

Juntando as configurações.
```
          readinessProbe:
            httpGet:
              path: /healthz
              port: 9000
            periodSeconds: 3
            failureThreshold: 1
            timeoutSeconds: 1
            successThreshold: 1
            initialDelaySeconds: 10

          livenessProbe:
            httpGet:
              path: /healthz
              port: 9000
            periodSeconds: 5
            failureThreshold: 1
            timeoutSeconds: 1
            successThreshold: 1
            initialDelaySeconds: 10
```
**startupProbe**

Funciona somente no processo de verificação, quando fica pronto o readiness e o liveness começam a funcionar.

Tempo de tentativa periodSeconds X failureThreshold.
```
          startupProbe:
            httpGet:
              path: /healthz
              port: 9000
            periodSeconds: 3
            failureThreshold: 10
```
Aplciar alteração.
```
kubectl apply -f k8s/deployment.yaml && watch -n1 kubectl get pods
```
Sempre utilizar o startupProbe.

# Comandos

| **Comandos** | **Descrição** |
|----------|---------------|
| kubectl apply -f k8s/deploymente.yaml | Cria o replicaset que cria 
| kubectl apply -f k8s/pod.yaml | Cria um pod					| 
| kubectl apply -f k8s/replicaset.yaml | Cria um pod com replicas| 
| kubectl apply -f k8s/service.yaml | Inicia o service|
| kubectl delete goserver		| Delete o pod com o nome goserver | 
| kubectl delete replicaset goserver | Deleta o replicaset com o nome goserver
| kubectl describe pod <nome do pod>| Traz as informações do pod|
| kubectl exec -it goserver-dc545f85f-p2lpm -- bash | Modo iterativo |
| kubectl logs <nome> | Ver o log|
| kubectl get nodes 		    | Mostra os nodes  				|
| kubectl get po 			    | Mostra os pods				|
| kubectl get pods 				| Mostra os pods 				|
| kubectl get replicaset 				| Mostra como está replicado|
| kubectl get services | Mostra os services ativos, TYPE, CLUSTER-IP|
| kubectl get svc | Mostra os services ativos |
| kubectl port-forward svc/service-goserver 9000:9000| Libera a porta para o acesso do serviço|
| kubectl rollout undo deploymente goserver| Mostra as versões do código|
| kubectl rollout undo deployment goserver --to-revision=1| Volta para versão 1|
| watch -n1 kubectl get pods | Assitir o pods em execusão|