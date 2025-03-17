### Lancer le nouveau conteneur

Maintenant, exécute le conteneur avec :

```sh
docker run -p 8000:8000 -e MONGO_URI="mongodb://<USERNAME>:<PASSWORD>@ProjetCosmosDB.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb" detection-anomalies
```
### Si tu veux exécuter le conteneur en arrière-plan (mode détaché) :

```sh
docker run -d -p 8000:8000 -e MONGO_URI="mongodb://<USERNAME>:<PASSWORD>@ProjetCosmosDB.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb" detection-anomalies
```