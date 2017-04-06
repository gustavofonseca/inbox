Especificação de requisitos
===========================

Inbox é uma ferramenta que apoia o fluxo de trabalho de uma equipe de produção
da SciELO na ingestão de conteúdos para uma ou mais coleções. Trata-se de um
sistema baseado na web, para operação via computadores de mesa ou tablets
com tela superior a 10 polegadas. Deve ser acessível para a operação por
pessoas com deficiência visual (em algum grau).


Requisitos
----------

Os usuários tipo (Produtor de XML, Depositante) devem ser capazes de:

* Depositar pacotes de artigos por meio de conta FTP ou FTPS;
* Acompanhar o estado do depósito em relação ao fluxo de produção;
* Trocar mensagens com os analistas de qualidade a fim de solucionar questões
  relativas ao depósito;
* Submeter arquivos avulsos -- inéditos ou versões dos já existentes --
  relacionados ao pacote depositado;
* Gerenciar suas credenciais de acesso à conta FTP ou FTPS;
* Gerenciar suas credenciais de acesso ao sistema;
* Se organizar em, e gerir times de trabalho;
* Visualizar métricas e estatísticas das suas interações com o sistema de
  ingestão.


Os usuários tipo (Equipe de produção, Técnico, Analista de qualidade) devem
ser capazes de:

* Visualizar os artigos pendentes de validação designados para si;
* Visualizar todos os artigos de todos os pacotes de todos os depósitos;
* Iniciar o processo de validação de um artigo;
* Tratar o conjunto de todos os arquivos que compõem um artigo como uma
  unidade de trabalho;
* Visualizar a lista de verificação;
* Completar cada etapa da lista de verificação;
* Solicitar correção em determinado arquivo;
* Enviar e responder mensagens para os depositantes a fim de solucionar questões
  relativas ao depósito;
* Interromper temporariamente o processo de validação de um artigo;
* Concluir o processo de validação de um artigo;
* Designar artigos pendentes de validação para outros profissionais;
* Gerenciar a lista de verificação (admin apenas);
* Gerenciar usuários (admin apenas);
* Gerenciar times de trabalho (admin apenas)
* Convidar usuário a se registrar no sistema como dono de time de trabalho;
* Visualizar métricas e estatísticas das suas interações com o sistema de
  ingestão e outras estatísticas avançadas;


Depósito
~~~~~~~~
O depósito de um pacote SciELO PS para ingresso na coleção.

Possui os atributos: (1) número de protocolo relacionado, que deve ser único na
instalação, (2) nome do time de trabalho responsável pelo depósito, (3) data
e hora do depósito, e (4) estado em que se encontra em relação ao fluxo de
ingestão.

Os estados possíveis são: depositado, em processo, concluído e
rejeitado.

De maneira rasa e objetiva, o depósito serve como formalização do recebimento
de um pacote de artigos.


Pacote
~~~~~~
Pacote depositado para inclusão na coleção.

É basicamente um maço, zipado, de arquivos XML e seus respectivos ativos
digitais, incluindo PDF.

Um pacote é uma estrutura aberta que pode receber novos membros inéditos ou
novas versões dos já existentes.


Membro do pacote
~~~~~~~~~~~~~~~~
Representa a existência de um arquivo no pacote, independentemente da sua
versão, e está vinculado a uma quantidade arbitrária de versões do membro do
pacote.

Possui o atributo nome, que armazena um texto referente ao nome do arquivo.


Versão do membro do pacote
~~~~~~~~~~~~~~~~~~~~~~~~~~
Representa uma versão do arquivo membro do pacote. As versões são ordenadas
com base na sua data e hora de criação.

É proibida qualquer manipulação ou edição no conteúdo dos arquivos representados
aqui, sendo necessária a criação de novas versões.


Artigo
~~~~~~
Representa um conjunto de membros de um pacote, interrelacionados, que
formam um único artigo/trabalho científico/documento/unidade publicável.

É formado por Conteúdo do artigo (XML SciELO PS) e todos os seus arquivos
vinculados (Ativo do artigo).


Conteúdo do artigo
~~~~~~~~~~~~~~~~~~
É um membro do pacote que representa um artigo codificado em XML de acordo
com a especificação SciELO PS.

Especializa o tipo de entidade Membro do pacote.


Ativo do artigo
~~~~~~~~~~~~~~~
É um membro do pacote que representa um arquivo parte do Artigo, referenciado
no conteúdo do artigo ou não.

São exemplos: imagens, pdf, planilhas, multimídia.


Visualização do Artigo
~~~~~~~~~~~~~~~~~~~~~~
Os artigos podem ser visualizados de maneiras distintas, permitindo que
os usuários alternem entre os modos: (1) código fonte, (2) galeria e (3) html.

Por padrão, é aplicado o modo código fonte de visualização, onde o analista de
qualidade poderá navegar pela estrutura do documento para validação em nível
de metadado.

O modo galeria permite a visualização dos ativos do artigo como em uma galeria
de midia (tipo carrossel), onde o analista de qualidade poderá navegar entre os
ativos, ter acesso aos seus metadados -- Exif, XMP e IPTC -- e sua
pré-visualização.

Por último o modo html que, como o nome sugere, apresenta o artigo formatado
para que seja possível visualizar o artigo de maneira semelhante a que será
publicado.

