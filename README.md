# plotmon
Monitors a Spacemesh Plotter. Currently only supports a single GPU. If you have multi-GPU it will only show the provider 0. It should still work but you won't get stats on each GPU. I will add multi-GPU support in the future.

### Install Venv

##### Ubuntu
```
sudo apt install python3.10-venv
```

### Create Virtual Environment

```
python3 -m venv env
```

### Activate Virtual Environment

##### Linux
``` 
source env/bin/activate
```

##### Windows
``` 
source env/Scripts/activate
```

### Install Requirements

```
pip install -r requirements.txt
```

### Update Config

```
{"post_data_dir": <YOUR POST DATA DIR>}
```
