# pywsvisualization
Python Package to visualization Human robot interaction in Virtual workspace

## Development

### Python3.x

1. Create a Virtual Environment
   
    ```bash
   $ virtualenv -m venv venv
   ```
   
2. Activate Virtual Environment

    ```bash
    $ . venv/bin/activate 
    ```

3. Install the Dependencies

    ```bash
    $ pip install -r requirements.txt
    ```

4. Install `pywsvisualization` as python package for development:

    ```bash
   $ pip install -e .
   ```
   
   This makes the `ws-visualization` binary available as a CLI

### Usage
Run `ws-visualization` binary on command line:

- -c : configuration file path/name

```bash
$ ws-visualization -c config.yaml
```

### Message Broker (RabbitMQ)

Use the [rabbitmqtt](https://github.com/virtual-origami/rabbitmqtt) stack for the Message Broker

__NOTE__: The `rabbitmqtt` stack needs an external docker network called `iotstack` make sure to create one using `docker network create iotstack`

### Docker

1. To build Docker Images locally use:

    ```bash
    $ docker build -t pywsvisualization:<version> .
    ```

2. To run the Application along with the RabbitMQ Broker connect the container with the `iotstack` network using:

    ```bash
    $ docker run --rm --network=iotstack -t pywsvisualization:<version> -c config.yaml
    ```

    __INFO__: Change the broker address in the `config.yaml` file to `rabbitmq` (name of the RabbitMQ Container in _rabbitmqtt_ stack)

3. To run the a custom configuration for the Container use:

    ```bash
    $ docker run --rm -v $(pwd)/config.yaml:/pywsvisualization/config.yaml --network=iotstack -t pywsvisualization:<version> -c config.yaml
    ```
