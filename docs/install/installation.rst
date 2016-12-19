Guia de instalação
==================

Contêineres Docker
------------------

A base de códigos já vem pré-configurada de tal forma que a construção e
execução da instância local de desenvolvimento pode ser realizada por
meio dos comandos:

.. code-block:: bash

    docker-compose -f dev.yml build
    docker-compose -f dev.yml up


Nesse momento a aplicação web deve estar respondendo na URL
``http://localhost:8000``. É importante notar que o setup da instância de
desenvolvimento é composto pelos contêineres *django* e *postgres*, excluíndo os
que desempenham tarefas assíncronas, verificação anti-virus e tal.

A execução de comandos administrativos, como por exemplo os para a migração do
banco de dados, pode ser realizada conforme o exemplo:

.. code-block:: bash

    docker-compose -f dev.yml run django python manage.py help


Mais conveniência com Makefile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O uso do docker-compose durante o processo de desenvolvimento pode ser
trabalhoso e exigir a digitação de longas linhas de comando no console. Para
facilitar um pouco mais esse processo você poderá utilizar o Makefile
disponibilizado na raíz do projeto. As tarefas disponíveis são:

* start:  docker-compose -f dev.yml up -d
* stop:   docker-compose -f dev.yml stop
* test:   docker-compose -f dev.yml run --rm django python manage.py test --failfast
* status: docker-compose -f dev.yml ps
* clean:  docker-compose -f dev.yml rm
* shell:  docker-compose -f dev.yml run --rm django python manage.py shell_plus
* build:  docker-compose -f dev.yml build
* logs:   docker-compose -f dev.yml logs -f

.. code-block:: bash

    gustavofonseca@PAT113-SCIELO-2:inbox make start
    Creating inbox_redis_1
    Creating inbox_postgres_1
    Creating inbox_django_1


Visão geral dos serviços envolvidos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------+-------+-----------------------------------------------------+
| Serviço   | Porta | Descrição                                           |
+===========+=======+=====================================================+
| django    | 5000  | Aplicação web executada pelo *gunicorn*             |
+-----------+-------+-----------------------------------------------------+
| nginx     | 80    | Proxy reverso                                       |
+-----------+-------+-----------------------------------------------------+
| redis     | 6379  | Cache e broker de mensagens assíncronas             |
+-----------+-------+-----------------------------------------------------+
| postgres  | 5432  | Banco de dados                                      |
+-----------+-------+-----------------------------------------------------+
| clamav    | 3310  | antivirus                                           |
+-----------+-------+-----------------------------------------------------+


Volumes:

+-----------------+------------------+------------------------------------+
| Nome            | Contêiner        | Destino (contêiner)                |
+=================+==================+====================================+
| postgres_data   | postgres         | /var/lib/postgresql/data           |
+-----------------+------------------+------------------------------------+
| postgres_backup | postgres         | /backups                           |
+-----------------+------------------+------------------------------------+
| django_media    | django           | /app/inbox/media              |
+-----------------+------------------+------------------------------------+


Principais variáveis de ambiente:

* POSTGRES_USER
* POSTGRES_PASSWORD

