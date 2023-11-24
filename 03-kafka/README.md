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