**Activate the virtual environment**

```
source blockchain-env/scripts/activate
```

**Install all packages**

```
pip3 install -r requirements.tx

```

**Add private subscribe and publish keys from PubNub**

add .env file to the backend folder with the following format:

```
subscribe_key = <SUBSCRIBE_KEY>
publish_key = <PUBLISH_KEY>
```

**Run the tests**

Make sure to activate the virtual environment

```
python -m pytest backend/tests
```

**Run the application and API**

Make sure to activate the virtual environment

```
python -m backend.app
```

**Run a peer instance**

```
export PEER=True && python -m backend.app
```