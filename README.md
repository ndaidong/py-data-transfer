# py-data-transfer
Try some ways to transfer data in Python


# System requirements

- Ubuntu 18.04 or newer
- Python 3.6.5 or newer


# Setup

```bash
git clone https://github.com/ndaidong/py-data-transfer.git
cd  py-data-transfer
python3 -m venv venv
source venv/bin/activate
(venv) pip install -r requirements.txt
```

# Usage

There are sub folders in this repo:

- autobahn
- pure-python-udp
- pure-python-tcp
- python-socketio

In each of folder, we have 2 files `server.py` and `client.py`.
`server.py` and `client.py` should be ran at the different machines.
However, running them on the same machine is also good to start.

With each of method, we please run `server.py` first, for example in a terminal tab:

```bash
cd /path/to/py-data-transfer
source venv/bin/activate
(venv) python python-socketio/server.py
```

Then, we start `client.py` at another tab:

```bash
cd /path/to/py-data-transfer
source venv/bin/activate
(venv) python python-socketio/client.py
```

Check these 2 tabs to see the result.


We can specify HOST and PORT as regular environment variables:

```bash
# server
(venv) PORT=8182 python python-socketio/server.py

# client must connect to the same port
(venv) PORT=8182 python python-socketio/client.py

# if server is running at another IP
(venv) HOST=192.168.1.170 PORT=8182 python python-socketio/client.py
```


# Screenshots

Client:

![](https://i.imgur.com/FeqFBat.png)



Server:

![](https://i.imgur.com/6lFoNGY.png)




# License

The MIT License (MIT)
