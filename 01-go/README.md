<h1 align="center">
  <img src="../image/k8s-logo.png" alt="Kubernetes" width=120px height=120px >
  <br>
  Kubernetes - Gerenciando um Server em Go
</h1>

<div align="center">

[![Status](https://img.shields.io/badge/version-1.0-blue)]()
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

1. [Iniciando o cluster Kubernetes](#iniciando-o-cluster-kubernetes)<br>
  1.1 [Criando o servidor web em Go](#criando-o-servidor-web-em-go)<br>
  1.2 [Construindo a Imagem](#construindo-a-imagem)<br>
2. [Pod](#pod)<br>
  2.1 [Replica Set](#replica-set)<br>
  2.2 [Deployment](#deployment)<br>
  2.3 [Rollout](#rollout)<br>
3. [Acessando o Services](#acessando-o-services)<br>
  3.1 [Proxy](#proxy)<br>
  3.2 [Variáveis de Ambiente](#variáveis-de-ambiente)<br>
  3.3 [Config Map](#config-map)<br>
  3.4 [Secret](#secret)<br>
4. [Health Check](#health-check)<br>
5. [Auto Scaling](#auto-scaling)<br>
6. [Recursos do Node](#recursos-do-node)<br>
7. [HPA (Horizontal Pod Autoscaler)](#hpa-horizontal-pod-autoscaler)<br>
8. [Remoção do erro](#remoção-do-erro)<br>
9. [Teste de Estresse](#teste-de-estresse)<br>
10. [Armazenamento](#armazenamento)<br>
11. [Statefulset](#statefulset)<br>
12. [Ingress](#ingress)<br>
13. [Certificado TLS](#certificado-tls)<br>
14. [Name Space](#name-space)<br>
15. [Context](#context)<br>
16. [Service Account](#service-account)<br>
17. [Comandos](#comandos)<br>


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
	http.ListenAndServe(":8080", nil)

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
Build da imagem e push utilizando Docker.

```
docker build -t faelk8/hello-go . && docker push faelk8/hello-go:v1

```

Executar o container liberando a porta 8080.
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
* Deployment cria o replicaset que cria o pod.
* Quando muda a versão do deployment ele derruba tudo e cria com a nova versão.
* Resolve o problema do replica set.

Para criar um deployment basta mudar o valo do **kind: Deployment**.

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
    port: 8080
    protocol: TCP
```

**name: serivce-goserver =  host**

Comando para iniciar.
```
kubectl apply -f k8s/service.yaml
```

O service foi iniciado mas o acesso ainda precisa ser liberado, o comando libera o acesso na porta 8080.
```
kubectl port-forward svc/service-goserver 8080:8080
```
http://localhost:8080

**Target Port**

Redirecionamento de porta. Quando acessar a porta 8080 o service redireciona para a porta 5000 do container.

service.go
```
func main() {
	http.HandleFunc("/", Hello)
	http.ListenAndServe(":5000", nil)

}
```

Aplicando alteração.
```
kubectl apply -f k8s/service.yaml
```
Comando para acesso.
```
kubectl port-forward svc/service-goserver 8080:8080
```

service.yaml
```
  - name: goserver-service
    port: 8080
    targetPort: 5000
    protocol: TCP
```

**NodePort**

Quando tem várias nodes trabalhando e se tem um acesso por uma porta específica todos os nodes liberam o acesso para aquela porta que vai entrar no serviço.

Utilizado para testes e serviços temporários.

service.yaml
```
  - name: goserver-service
    port: 8080
    protocol: TCP
    nodePort: 300001 #30.000 32.767
```

Aplicando alteração.
```
kubectl apply -f k8s/service.yaml
```

Comando para acesso.
```
kubectl port-forward svc/service-goserver 8080:8080
```

**Load Balancer**

Gera um IP para acessar a aplicação de fora, utiizando para nuvem. Gera um PORT.

service.yaml
```
  type: LoadBalancer
```
Aplicando alteração.
```
kubectl apply -f k8s/service.yaml
```

Comando para acesso.
```
kubectl port-forward svc/service-goserver 8080:8080
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
Aplicando a atualização.
```
docker  build -t faelk8/hello-ho:v1.1 . && dockr push faelk8/hello-go:v1.1

kubeclt apply -f k8s/deployment.yaml
```
Acessando o serviço.
```
kubectl port-forward svc/service-goserver 8080:8080
```

# Config Map
Mapeando variáveis de ambiente.

Forma mais simples.

configmap-env.yaml
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
kubectl port-forward svc/service-goserver 8080:8080
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
kubectl port-forward svc/service-goserver 8080:8080
```

Forma mais avançada, carrega todas as variáveis de ambiente. Substitui o deployment anterior.

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
kubectl port-forward svc/service-goserver 8080:8080
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

Aplicando alteração:
```
docker build -t faelk8/hello-go:v1.4 . && docker push faelk8/hello-go:v1.4
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
Kubectl port-forward svc/service-goserver  8080:8080
```
**Acessar:**  www.localhost:8080/secret

# Health Check
Verificar a saúde da aplicação. Até 25 segundos vai estar funcionando, depois vai apresentar erro, porém continua rodando.

## Liveness
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
Kubectl port-forward svc/service-goserver  8080:8080
```

## LivenessProbe

```
      containers:
        - name: goserver
          image: faelk8/hello-go:1.5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            periodSeconds: 5
            failureThreshold: 3
            timeoutSeconds: 1
            successThreshold: 1
```

Aplicando alteração e assistir os pods.
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
              port: 8080
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
              port: 8080
            periodSeconds: 3
            failureThreshold: 1
            timeoutSeconds: 1
            successThreshold: 1
            initialDelaySeconds: 10

          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
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
              port: 8080
            periodSeconds: 3
            failureThreshold: 10
```
Aplciar alteração.
```
kubectl apply -f k8s/deployment.yaml && watch -n1 kubectl get pods
```
Sempre utilizar o startupProbe.

# Auto Scaling
Instalar o metrics server

Repositório https://github.com/kubernetes-sigs/metrics-server

Baixar https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

```
cd k8s
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
Renomear para metrics-server.yaml

No deploymente do metrics-server.yaml adicionar **- --kubelet-insecure-tls**

Aplicando alteração
```
kubectl apply -f metrics-server.yaml
kubectl get apiservices # ver se está funcionando
```
Na saída do terminal precisa ter o **v1beta1.metrics.k8s.io** para confirmar que está ativo.

# Recursos do Node

Recurso mínimo para o funcionamento que fica reservado para o sistema. Levar em consideração a quantidade disponível do computador e tomar cuidado com a memória.
```
          resources:
            requests: 
              cpu: 100m
              memory: 20Mi
            limits:
              cpu: 500m
              memory: 25Mi
```
Ver o consumo de recursos
```
kubectl top pod < nome do pod >
```

# HPA
Escla de forma horizontal, adiocando novos pods de acordo com o programado.

hpa.yaml
```
metadata:
  name: hpa-goserver
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: goserver
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 35
```

# Remoção do erro
server.go
```
func Healthz(w http.ResponseWriter, r *http.Request) {
	duration := time.Since(startedAt)
	if duration.Seconds() < 10 {
		w.WriteHeader(500)
		w.Write([]byte(fmt.Sprintf("Duração: %v", duration.Seconds())))
	} else {
		w.WriteHeader(200)
		w.Write([]byte("ok"))
	}
}
```
Trocar a imagem no deployment.yaml
```
image: faelk8/hello-go:1.8
```
Aplicando alteração.
```
docker build -t faelk8/hello-go:1.8  . && docker push faelk8/hello-go:1.8
kubectl apply -f k8s/deployment.yaml
```

# Teste de Estress
Criando um pod para o teste.

```
kubectl run fortio --image=fortio/fortio --restart=Never --  load -qps 800 -t 120s -c 70 "http://service-goserver/healthz"

```
Explicação do comando:
* kubectl run -it --generator=run-pod/v1: Gera um pod
* fotio: Nome do pod
* --rm: Remove quando o processo acabar
* --image=fortio/fortio: Imagem do fortio
* -- load -qps 800 -t 120s -c 70 "http://service-goserver/healthz" : Comando dentro do pod que executa 800 requisições por segundo por 120 segundos com 70 conexões simultâneas no endereço http://service-goserver/healthz

# Armazenamento
StorageClass disponibiliza um espaço em disco.
* ReadWriteOnce: Pode ler, gravar desde que esteja no mesmo node.

Documentação: https://kubernetes.io/docs/concepts/storage/persistent-volumes/

Persistência

pvc.yaml
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: goserver-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```
deployment.yaml
```
          ...
          volumeMounts:           
            - mountPath: "/go/pvc"
              name: goserver-volume
              ...
      volumes:
        - name: goserver-volume
          persistentVolumeClaim: 
            claimName: goserver-pvc
            ...
```
Aplicando alteração
```
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl get pvc # mostra os discos
```

# Statefulset
Banco de dados com armazenamento em disco.

statefulset.yaml
```
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  replicas: 3
  serviceName: mysql-h
  selector:
      matchLabels:
        app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: root
          volumeMounts:
            - mountPath: /var/lib/mysql
              name: mysql-volume

  volumeClaimTemplates:
  - metadata:
      name: mysql-volume
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 5Gi
```
**"LoadBalance"** Com essa opção pode escolher o banco para gravar e outro para ler.

service-mysql-h.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: mysql-h
spec:
  selector:
    app: mysql
  ports:
  - port: 3306
  clusterIP: None
```
Aplicando alteração
```
kubectl apply -f k8s/statefulset.yaml
kubectl apply -f k8s/service-mysql-h.yaml
```

# Ingress
Cria um ponto único de acesso que faz roteamento para cada serviço. Atua como um load balancer com um IP. Por exemplo se tiver 5 serviços, quando acesssar o IP baseado no host name e no path encaminha para o serviço de acordo com o path.
* IP/admin - Envia para o serviço admin;
* IP/ajuda - Envia para o serviço ajuda;
* IP/busca - Envia para o serviço busca;

Lembra uma api gateway que faz o reteamento. 

Proxy reverso que pega requisição e roteia para onde precisa.

## Instalação

Para ambiente em nuvem. Precisa acessar o serviço e enviar os arquivos.
```
kubectl apply -f k8s/
```
Após tudo rodando é possível ver o service rodando e ver o **EXTERNAL-IP**. Aplicação vai estar rodando no IP.
```
kubectl get svc
```
### ingress-nginx
Instalar de acordo com a aplicação.

Após instalação vai ter um **EXTERNAL-IP** que vai passar a ser usado.

Código para a criação do ingress, quando acessar o serviço é encaminhado para o porta 8080.

ingress.yaml
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-host
  labels:
    name: ingress-host
  annotations:
    kubernetex.io/ingress.class: "nginx" # Adaptador
spec:
  rules:
  - host: "exemplo.com.br"
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: service-goserver
            port: 
              number: 8080
```
Aplicando alteração.
```
kubectl apply -f k8s/ingress.yaml
```
Colocar o **EXTERNAL-IP** no DNS da nuvem.

service.yaml pode alterar para **type: Cluster IP** para economizar. Precisa deletar e criar novamente e não vai ter o **EXTERNAL-IP**.

# Certificado TLS
Esse certificado é gratuito e quando expirado é renovado de forma automática.

Seguir os passos para instalação.

https://cert-manager.io/docs/installation/kubectl/

Comando para ver
```
kubectl get po -n cert-manager
```

cluster-issuer.yaml
```
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt
  namespace: cert-manager
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: meu@email.com
    privateKeySecretRef:
      name: letsencrypt-tls # nome que preferir
    solver: 
      - http01:
        ingress: 
          class: nginx
```

Alteração do ingress.
ingress.yaml
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-host
  labels:
    name: ingress-host
  annotations:
    kubernetex.io/ingress.class: "nginx" # Adaptador
    cert-manager.io/cluster-issuer: letsencrypt
    ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  rules:
  - host: "exemplo.com.br"
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: service-goserver
            port: 
              number: 8080
  tls:
  - hosts:
    - "exemplo.com.br"
    secretName: letsencrypt-tls
```


Aplicando a alteração
```
kubectl apply -f k8s/cluster-issuer.yaml
kubectl apply -f k8s/ingress.yaml
kubectl get certificates # mostra os certificados
```
Para ver os detalhes do certificado informando seu nome.
```
kubectl describe certificate letsencrypt-tls
```

# Name Space
Recomendado ter um cluster para ambiente de desenvolvimento e um para produção. Na falta de recursos ter names spaces separados em desenvolvimento e produção.

**Apartir desse pontos comando executados dentro da pasta namespace.**

Criando um name space de dev-kafka.
```
kubectl create ns dev-kafka
```
Quando for aplicar um novo deploymente basta incluir no final **-n=dev-kafka**:
```
kubectl apply -f k8s/deployment.yaml -n=dev-kafka
```
Olhando os pods no name espace:
```
kubectl get po -n=dev-kafka
```
Para ver todos os pods que tem o server:
```
kubectl get pods -l app=server
```
Outra forma é informar na especificação o name space.

# Context
Utilizado para separação em ambiente de desenvolvimento e produção.

Para ver as configurações no **contexts** disponíveis.
```
kubectl config view
```
Criando um context:
```
kubectl config set-context dev --namespace=dev --cluster=jota --user=jota

kubectl config set-context dev --namespace=prod --cluster=jota --user=jota
```

Ativando o context:
```
kubectl config use-context dev
```

# Service Account
Configurando as permissões para o name space.

security.yaml
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: server

---

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: server-read
rules:
- apiGroups: [""]
  resources: ["pods","services"] # o que pode trabalhar
  verbs: ["get","watch","list"] # o que pode fazer
- apiGroups: ["apps"]
  resources: ["deployments"] # o que pode trabalhar
  verbs: ["get","watch","list"] # o que pode fazer

--- 

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: server-read-bind
subjects:
- kind: ServiceAccount
  name: server
  namespace: prod
roleRef:
  kind: Role
  name: server-read
  apiGroup: rbac.authorization.k8s.io/v1
```
Editar o deployment antes do container.
deployment.yaml
```
...
spec:
  serviceAccount: server
```

Aplicando alteração:
```
kubectl apply -f security.yaml
kubectl apply -f deployment.yaml
```

Para permissão em todo o cluster altere o kind para **ClusterRole** e **ClusterRoleBinding**.

# Comandos

| **Comandos** | **Descrição** |
|----------|---------------|
| kubectl api-resources | Mostra  os recursos |
| kubectl apply -f k8s/deploymente.yaml | Cria o replicaset que cria 
| kubectl apply -f k8s/pod.yaml | Cria um pod					| 
| kubectl apply -f k8s/replicaset.yaml | Cria um pod com replicas|  
| kubectl apply -f k8s/service.yaml | Inicia o service |
| kubectl config get-contexts | Mostra todos os cluster |
| kubectl config use-context  | Mostra o cluster atual |
| kubectl config use-context < nome do serivço > | Para trocar de cluster |
| kubectl delete goserver		| Delete o pod com o nome goserver | 
| kubectl delete replicaset goserver | Deleta o replicaset com o nome goserver |
| kubectl delete statefulset < nomem > | Deleta o statefulset |
| kubectl describe pod < nome do pod >| Traz as informações do pod |
| kubectl exec -it goserver-dc545f85f-p2lpm -- bash | Modo iterativo |
| kubectl logs < nome > | Ver o log|
| kubectl get certificates 				| Mostra os certificados instalados |
| kubectl get nodes 		    | Mostra os nodes  				|
| kubectl get ns 		    | Mostra os names espace  				|
| kubectl get po 			    | Mostra os pods				|
| kubectl get pods 				| Mostra os pods 				|
| kubectl get pods l- app=server | Mostra todos os pods com o nome server, independente do name space	|
| kubectl get replicaset 				| Mostra como está replicado |
| kubectl get services | Mostra os services ativos, TYPE, CLUSTER- IP|
| kubectl get storageclass | Mostra os disco disponíveis |
| kubectl get svc | Mostra os services ativos |
| kubectl port-forward svc/service-goserver 8080:8080 | Libera a porta para o acesso do serviço |
| kubectl rollout undo deploymente goserver | Mostra as versões do código |
| kubectl rollout undo deployment goserver --to-revision=1 | Volta para versão 1|
| kubectl scale statefulset mysql --replicas=5 | Replica de forma manual sem ordem |
| kubectl top pod <nome do pod> | Mostra o quanto de recurso está sendo consumido |
| watch -n1 kubectl get pods | Assitir o pods em execução |

## Configurações
| **Comandos** | **Descrição** |
|----------|---------------|
| cat ~/.kube/config | Mostra as configurações |
| kubectl config view| Mostra as configurações do cluster do name space default |