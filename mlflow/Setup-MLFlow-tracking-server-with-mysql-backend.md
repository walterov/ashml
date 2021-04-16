# Setup MLFlow tracking server with mysql backend on Ubuntu 18.04 Virtual Machine

By following this guide, you will set up mlflow tracking server with mysql backend.

## Prerequisites

1.   Virtual Machine with Ubuntu 18.04


## Install pip3

<pre>$ sudo apt-get update</pre>

<pre> $ sudo apt-get -y install python3-pip
</pre>

You may verify pip3 installation:

```
 ~$ pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)

 ~$ which pip3
/usr/bin/pip3
```

## Install mlflow

```
pip3 install mlflow
```

You may find the location of installation by:

``` 
~$ pip3 show mlflow 

Name: mlflow
Version: 1.15.0
Location: /home/azureuser/.local/lib/python3.6/site-packages
```

mlflow command line binary is in ~/.local/bin. Let's update the PATH environment variable:

```
~$ export PATH=$PATH:~/.local/bin

```

## Install mysql and set up mysql user

1. [Install mysql 8.0 on ubuntu 18.04](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/#apt-repo-fresh-install)

After installation of mysql 8.0, you will be able to connect mysql by

```sudo mysql ```


2. Create mysql user

```
sudo mysql

CREATE USER 'mlflow'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON * . * TO 'mlflow'@'localhost';

```

3.  Create mysql database named "mlflow"

You may connect to mysql using user created above, then create a database with name "mlflow"

```
mysql -u mlflow -p

```

then enter password to connect to mysql

```
mysql> CREATE DATABASE mlflow;

```

## Install mysql python driver

```
pip3 install mysql-connector-python

```

## Launch mlflow tracking server

First, you need a directory for storing mlflow artifacts. Let's create a directory:

```
~$ mkdir mlruns
```

Now we can launch a mlflow server with mysql backend as following (replace password with your own):

```
mlflow server --backend-store-uri mysql+mysqlconnector://mlflow:password@127.0.0.1:3306/mlflow --default-artifact-root ./mlruns
```

For the first time launching, you may see something like:

```
2021/04/02 01:01:09 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2021/04/02 01:01:09 INFO mlflow.store.db.utils: Updating database tables
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 451aebb31d03, add metric step
INFO  [alembic.runtime.migration] Running upgrade 451aebb31d03 -> 90e64c465722, migrate user column to tags
INFO  [alembic.runtime.migration] Running upgrade 90e64c465722 -> 181f10493468, allow nulls for metric values
INFO  [alembic.runtime.migration] Running upgrade 181f10493468 -> df50e92ffc5e, Add Experiment Tags Table
INFO  [alembic.runtime.migration] Running upgrade df50e92ffc5e -> 7ac759974ad8, Update run tags with larger limit
INFO  [alembic.runtime.migration] Running upgrade 7ac759974ad8 -> 89d4b8295536, create latest metrics table
INFO  [89d4b8295536_create_latest_metrics_table_py] Migration complete!
INFO  [alembic.runtime.migration] Running upgrade 89d4b8295536 -> 2b4d017a5e9b, add model registry tables to db
INFO  [2b4d017a5e9b_add_model_registry_tables_to_db_py] Adding registered_models and model_versions tables to database.
INFO  [2b4d017a5e9b_add_model_registry_tables_to_db_py] Migration complete!
INFO  [alembic.runtime.migration] Running upgrade 2b4d017a5e9b -> cfd24bdc0731, Update run status constraint with killed
INFO  [alembic.runtime.migration] Running upgrade cfd24bdc0731 -> 0a8213491aaa, drop_duplicate_killed_constraint
INFO  [alembic.runtime.migration] Running upgrade 0a8213491aaa -> 728d730b5ebd, add registered model tags table
INFO  [alembic.runtime.migration] Running upgrade 728d730b5ebd -> 27a6a02d2cf1, add model version tags table
INFO  [alembic.runtime.migration] Running upgrade 27a6a02d2cf1 -> 84291f40a231, add run_link to model_version
INFO  [alembic.runtime.migration] Running upgrade 84291f40a231 -> a8c4a736bde6, allow nulls for run_id
INFO  [alembic.runtime.migration] Running upgrade a8c4a736bde6 -> 39d1c3be5f05, add_is_nan_constraint_for_metrics_tables_if_necessary
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
[2021-04-02 01:01:12 +0000] [25085] [INFO] Starting gunicorn 20.1.0
[2021-04-02 01:01:12 +0000] [25085] [INFO] Listening at: http://127.0.0.1:5000 (25085)
[2021-04-02 01:01:12 +0000] [25085] [INFO] Using worker: sync
[2021-04-02 01:01:12 +0000] [25088] [INFO] Booting worker with pid: 25088
[2021-04-02 01:01:12 +0000] [25089] [INFO] Booting worker with pid: 25089
[2021-04-02 01:01:12 +0000] [25091] [INFO] Booting worker with pid: 25091
[2021-04-02 01:01:12 +0000] [25092] [INFO] Booting worker with pid: 25092

```

The server is listening at port 5000

To log the runs to this server, you just need to

```
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")

```