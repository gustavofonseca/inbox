penne_core
==========

*Penne* é o codinome do projeto de software para modernizar o fluxo de 
ingestão de conteúdos de uma coleção da rede SciELO. Consiste atualmente de 
2 componentes:

* penne_shell: realiza a interface com o usuário durante o processo de depósito 
  dos pacotes de artigos, por meio de um servidor FTP.
* penne_core: registra os depósitos dos pacotes e implementa os fluxos de 
  verificação e controle de qualidade para o ingresso na coleção.



Implantação com Docker
----------------------

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
| django_media    | django           | /app/penne_core/media              |
+-----------------+------------------+------------------------------------+


Principais variáveis de ambiente:

* POSTGRES_USER
* POSTGRES_PASSWORD

