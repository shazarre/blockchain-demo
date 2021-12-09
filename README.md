# Simple blockchain implementation demo

## How it works?

* Run 3 docker containers with the app: `make start`
* Setup the connectivity between the nodes: `make setup`
* Run
```
curl --request POST \
  --url http://127.0.0.1:5001/transaction \
  --header 'Content-Type: application/json' \
  --data '{
	"uuid": "862dda36-e1c0-451e-84e4-8599cbc21295",
	"sender": "abcd",
	"receiver": "efgh",
	"amount": 100
}'
```

to create a transaction on the first node.

* Run
```
curl --request GET --url http://127.0.0.1:5002/mine
```

to mine new block on the second node.

* Run 
```
curl --request GET --url http://127.0.0.1:5003/chain
```

to fetch the chain from the third node.

If all worked well, you should see that transactions and blocks are
synced between all the nodes.

## Local development

* Copy `.envrc.dist` to `.envrc` (assuming you're using [direnv](https://direnv.net/), otherwise 
  you need to provide required env vars in different way)
* Run `venv/bin/python -m flask run` to start the app
