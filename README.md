# Flask HW №1
![flake8](https://github.com/EgorikA4/709_22_2/actions/workflows/pylint.yml/badge.svg?branch=flask_project)

## Installation
1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script).
2. Clone the repository and go to the `flask_hw` branch.
    ```bash
    # clone repository
    git clone https://github.com/EgorikA4/709_22_2.git

    # go to the repository folder
    cd 709_22_2/

    # switch to the 'flask_hw' branch
    git checkout flask_hw
    ```
3. Create `.env` file and specify the following variables:
    ```bash
    POSTGRES_HOST=host.docker.internal
    POSTGRES_PORT=38746
    POSTGRES_DB=postgres
    POSTGRES_USER=sirius_2024
    POSTGRES_PASSWORD=change_me

    FLASK_PORT=5000
    ```
4. Launch the docker container.
    ```bash
    docker compose up
    ```
    Launching the container in the detach mode.
    ```bash
    docker compose up -d
    ```
    Stop the containers.
    ```bash
    docker compose stop 
    ```
    Stop and delete containers.
    ```bash
    docker compose down
    ```

## How to launch the project in development mode.
1. Create and choose python [virtual enviroment](https://docs.python.org/3/library/venv.html).
    ```bash
    # create enviroment
    python3 -m venv venv/

    # choose enviroment
    source venv/bin/activate
    ```
2. Install requirements.
    ```bash
    pip install -r requirements/main_requiremenets.txt
    pip install -r requiremenets/dev_requiremenets.txt
    ```
3. Start the database.
    ```shell
    docker start flask_project-postgres-1
    ```

> [!NOTE]
> `flask_project` is a container created using the `docker compose up` command.

4. Launch the flask project.
    ```bash
    python3 hw/app.py
    ```
## Database [ER-schema](https://drive.google.com/file/d/1fsmQWRa5pgF0rLVxo-FUK4kUA1aIuq2k/view?usp=sharing)
