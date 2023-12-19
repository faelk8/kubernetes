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
Instalando Jaeger:

```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
```

Instalando Kiali:
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
```
Instalando Promethues:
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
```
Instalando Grafana:
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
```
Abrindo o dashboard:
```
istioctl dashboard kiali
```

# Conceitos Básicos
* Ingress ateway: Gerencia a entrada e a saída. Trabalha nos layes 4-6, garantindo o gerenciadomento de portas, host, e TLS. É concectado diretamente a um Virtual Service que será responsável pelo roteamento. Faz as requisiçôes de fora do cluster.
* Virtual Service: Permite configurar como as requisições serão roteadas para um serviço. Possoui uma série de regras que quando aplicadas farão com que a requisição seja direcioanda ao destino correto. Funciona como um roteador.
  * Roteamento
  * Subsets
  * Fault Injection
  * Retries
  * Timeout
* Destination Rules: Roteia o trágefo para um destino, então, usa as destination rules para configurar o que acontece com o tráfego quando chaga naquele destino.

# Solicitação
```
while true; do curl http://localhost:8000; echo; sleep 0.5; done;
```

# Circuit Breaking
Baixando:
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/httpbin/sample-client/fortio-deploy.yaml
```
Variável de ambiente:
```
export FORTIO_POD=$(kubectl get pods -l app=fortio -o 'jsonpath={.items[0].metadata.name}')
```
Executando o teste:
```
exec "$FORTIO_POD" -c fortio -- fortio load -c 2 -qps 0 -t 200s -loglevel Warning http://nginx-service:8000
```

# Virtual Service e Destination Rule
O `virtual-service.yaml` recebe a requisição e envia de acordo com as configurações onde o `destination-rule.yml` vai encaminhar para os pods.

#

#

#

#