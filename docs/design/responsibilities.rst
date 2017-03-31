Contratos e responsabilidades
=============================

Deposit
-------

O depósito de um pacote SciELO PS para ingresso na coleção.


+------------------+----------------------------------------------------------+
| Tipo:            | Classe concreta                                          |
+------------------+----------------------------------------------------------+
| Superclasses:    |                                                          |
+------------------+----------------------------------------------------------+

Responsabilidades:

    * Representa o esquema de persistência
    * Salva as alterações no banco de dados
    * Rotula e identifica um pacote depositado
    * Sabe o estado em que se encontra no fluxo de validação
    * Altera o seu estado no fluxo de validação


Package
-------

Um pacote é basicamente um maço, zipado, de arquivos XML -- que devem ser
válidos em relação a especificação SciELO PS -- e seus respectivos ativos
digitais, incluindo PDF.


+------------------+----------------------------------------------------------+
| Tipo:            | Classe concreta                                          |
+------------------+----------------------------------------------------------+
| Superclasses:    |                                                          |
+------------------+----------------------------------------------------------+

Responsabilidades:

    * Representa o esquema de persistência
    * Acessa o conteúdo do pacote
    * Expande o conteúdo do pacote  [PackageMember]
    * Cria novos membros


File
----

Um arquivo em disco.


+------------------+----------------------------------------------------------+
| Tipo:            | Classe abstract                                          |
+------------------+----------------------------------------------------------+
| Superclasses:    |                                                          |
+------------------+----------------------------------------------------------+

Responsabilidades:

    * Lê o seu conteúdo
    * Persiste o seu conteúdo
    * Infere seu mimetype
    * Informa seu tamanho em bytes


PackageMember
-------------

Um arquivo membro do pacote, nas suas multiplas versões.


+------------------+----------------------------------------------------------+
| Tipo:            | Classe concreta                                          |
+------------------+----------------------------------------------------------+
| Superclasses:    |                                                          |
+------------------+----------------------------------------------------------+

Responsabilidades:

    * Lê o seu conteúdo  [PackageMemberVersion]
    * Infere seu mimetype  [PackageMemberVersion]
    * Adiciona uma nova versão


PackageMemberVersion
--------------------

Um arquivo membro do pacote, em algum momento no tempo-espaço.


+------------------+----------------------------------------------------------+
| Tipo:            | Classe concreta                                          |
+------------------+----------------------------------------------------------+
| Superclasses:    |                                                          |
+------------------+----------------------------------------------------------+

Responsabilidades:


