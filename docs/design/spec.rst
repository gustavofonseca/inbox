Especificação de requisitos
===========================

Inbox é uma ferramenta que apoia o fluxo de trabalho de uma equipe de produção
da SciELO na ingestão de conteúdos para uma ou mais coleções. Trata-se de um
sistema baseado na web, para operação via computadores de mesa ou tablets
com tela superior a 10 polegadas. Deve ser acessível para a operação por
pessoas com deficiência visual (em algum grau).

Esse sistema incorpora responsabilidades que hoje estão distribuídas entre os
programas PTS, Title Manager, Converter e SciELO Manager, e o fluxo de trabalho
descrito no `Guia de Fluxebimento <https://drive.google.com/open?id=1ATdXOjQcEWL43wsTyjuGIrC9MAz6P2GwKLwCwt46PQc>`_
e `Check list - Fluxebimento <https://drive.google.com/open?id=1x9CLuDafl9zdqObHlHqITxZ-nCiuf49bXAeYAjXtImY>`_
(ambos os links possuem acesso restrito aos usuários @scielo.org). Essas
responsabilidades são:

* Controlar o recebimento de artigos registrando a data, a hora, o nome do
  depositante, nome do responsável e quais os artigos recebidos (PTS);
* Registrar o lote ou fascículo (PTS);
* Gerenciar dados do periódico e fascículo (Title/SciELO Manager);
* Intermediar toda a comunicação entre o analista de qualidade e o depositante
  (e-mails);
* Arquivar o conteúdo (Converter);


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
* Gerenciar times de trabalho (admin apenas);
* Convidar usuário a se registrar no sistema como dono de time de trabalho;
* Visualizar métricas e estatísticas das suas interações com o sistema de
  ingestão e outras estatísticas avançadas;


Depósito
````````
É o ponto de entrada de um pacote SciELO PS na coleção. Representa tanto a ação
quanto o objeto depositado.

O depositante receberá um número de protocolo referente ao depósito, que poderá
ser utilizado para consultar o estado em que o depósito se encontra em relação
ao fluxo de recebimento.

Possui minimamente os atributos: (1) número de protocolo relacionado, que deve
ser único na instalação, (2) nome do time de trabalho responsável pelo
depósito, (3) data e hora do depósito, e (4) estado em que se encontra em
relação ao fluxo de produção.

Os estados possíveis são: depositado, em processo, concluído e
rejeitado.

De maneira rasa e objetiva, o depósito serve como formalização do recebimento
de um pacote de artigos.


Pacote
``````
Pacote depositado para inclusão na coleção.

É basicamente um maço, zipado, de arquivos XML e seus respectivos ativos
digitais, incluindo PDF.

Pode ser que no pacote existam arquivos não referenciados por nenhum dos
XML presentes. Nesses casos, deverá haver uma intervenção manual por parte do
analista de qualidade indicando a qual Artigo o arquivo errante está relacionado.

Um pacote é uma estrutura aberta que pode receber novos membros inéditos ou
novas versões dos já existentes.


Membro do pacote
````````````````
Representa a existência de um arquivo no pacote, independentemente da sua
versão, e está vinculado a uma quantidade arbitrária de versões do membro do
pacote.

Possui o atributo nome, que armazena um texto referente ao nome do arquivo.


Versão do membro do pacote
``````````````````````````
Representa uma versão do arquivo membro do pacote. As versões são ordenadas
com base na sua data e hora de criação.

É proibida qualquer manipulação ou edição no conteúdo dos arquivos representados
aqui, sendo necessária a criação de novas versões.


Artigo
``````
Representa um conjunto de membros de um pacote, interrelacionados, que
formam um único artigo/trabalho científico/documento/unidade publicável.

É formado pelo conteúdo do artigo -- codificado em XML SciELO PS -- e todos os
seus arquivos vinculados (Ativo do artigo).


Conteúdo do artigo
``````````````````
É um membro do pacote que representa um artigo codificado em XML de acordo
com a especificação SciELO PS.


Ativo do artigo
```````````````
É um membro do pacote que representa um arquivo parte do Artigo, referenciado
no conteúdo do artigo ou não.

São exemplos: imagens, pdf, planilhas, multimídia.


Visualização do Artigo
``````````````````````
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


Comentários
```````````
Consiste de um ou mais parágrafos de texto, que pode ser formatado ou não,
imagens e referências a qualquer arquivo (versão do membro do pacote), pacote
ou depósito. Os comentários podem ser agrupados em forma de diálogos e marcados
como resolvidos.


Time de trabalho
````````````````
Agrupamento de usuários que depositam pacotes em nome de um único depositante,
cujo time dá o nome. O time de trabalho deve possuir no mínimo 1 usuário
afiliado, que será considerado dono do time. São permitidos multiplos donos
em um mesmo time. Não são permitidos usuários desfiliados de times, assim como
times sem afiliados.


Fluxo de recebimento
````````````````````
Sequência pré definida de atividades que objetivam garantir a qualidade
dos Artigos recebidos, por meio de validações automáticas e manuais, e
preparar o ambiente para o processo de arquivamento.

1. Verificação de estrutura e conteúdo (checklist fluxebimento);
2. Arquivamento.


Sistema de ingestão
```````````````````
Conjunto de entidades interligadas e interdependentes que cooperam em favor de
de um objetivo que é a ingestão de conteúdos.


Lista de verificação
````````````````````
Hoje chamada de *checklist fluxebimento*, trata-se de uma lista dos pontos
a serem verificados a fim de garantir a qualidade mínima necessária para que o
conteúdo seja aceito. A lista é composta por verificações de integridade e
consistência que podem variar de acordo com as políticas e critérios de cada
coleção.


Métricas, estatísticas e relatórios
```````````````````````````````````

1. Média de tempo de um artigo no fluxo de recebimento;
2. Número de problemas encontrados nos artigos, por editora/prestador;
3. Adoção da versão mais recente da SciELO PS;
4. Tamanho médio dos artigos (em KBytes);
5. Fascículos em atraso;


Subsistemas
-----------

* Subsistema de depósito: encapsula o processo de depósito de um pacote;
    * Subsistema de artigos: encapsula a representação de um Artigo;
    * Subsistema de validações: encapsula o fluxo de recebimento;
    * Subsistema de comentários: encapsula o mecanismo de troca de mensagens
      sobre determinado ponto a ser resolvido;
* Subsistema de visualização: encapsula a capacidade de produzir multiplas
  visualizações de um Artigo;
* Subsistema de arquivamento: define o modelo de dados em que os Artigos serão
  arquivados. Algo parecido com a Title Manager e o SciELO Manager;
* Subsistema de usuários: encapsula a estrutura e gestão dos times e usuários;


Classes candidatas
------------------

Aqui os nomes das classes começam a ser escritos em inglês a fim de estabelecer
termos e identificadores que serão utilizados na implementação.


Subsistema de depósitos:

* Deposit
* Package
* Package Member
* Package Member Version


Subsistema de artigos:

* Article (XML Data is an attribute)
* Asset
    * Image Asset
    * Video Asset
    * Audio Asset
    * External Link Asset


Subsistema de validações:

* Validation
    * Manual Validation
    * Automatic Validation
* Workflow
* Checklist
* Checkpoint


Subsistema de comentários:

* Issue
* Comment
    * Email Comment
    * Plain Comment
* Attachment


Subsistema de visualização:

* View
    * Source Code View
    * Gallery View
    * HTML View
* Metadata
    * Asset Metadata
        * Exif Metadata
        * XMP Metadata
        * IPTC Metadata
    * XML File Metadata (encoding, size, sps version, jats version)


Subsistema de arquivamento:

* Collection
* Journal
* Issue
    * Regular Issue
    * Special Issue
    * Supplement Issue
* Article
    * Bound Article
    * Ahead-of-print Article


Subsistema de usuários:

* Team
* User
    * QA Analyst
    * Depositor
* FTP Manager
* FTP Account


Anotações
`````````

* Entidades do tipo Collection são responsáveis por saber as políticas e critérios
  de aceite de conteúdo para suas respectivas coleções.
* O fluxo de trabalho é global para a instância ou pode variar de acordo com a
  coleção? Eu sugiro que seja único, pelo menos na primeira versão.


Atributos de qualidade
----------------------

**Pendente**

Diversas aplicações - *Cited-by*, *Production*, *Bibliometria*, *Ratchet*,
*Search* entre outras - tem como input os metadados dos artigos, e por vezes o
seu conteúdo. A tolerância a dados desatualizados varia de acordo com políticas
individuais, entretanto é desejável que a Inbox garanta a consistência
(Cada leitura recebe a mais recente escrita ou um erro).

A fim de prover uma margem de segurança em relação à capacidade operacional do
sistema, os atributos de qualidade que tratam do volume transacional ou outros
aspectos de capacidade devem ter seu valor multiplicado pelo *coeficiente de
escala* de valor `10`.

Com base num total de 1190 novos artigos por dia (190 * coeficiente de escala),
podemos realizar o seguinte cálculo:
`total_de_clientes * 0,04 artigos por segundo * 200.000 bytes por XML *
1 sentido => total_de_clientes * 8300 bytes/segundo`; Isso significa que para
140 aplicações o tráfego será de `9,3 Mbps`, apenas para o tráfego dos
metadados e texto completo.


* **Desempenho**  (latência e vazão/throughput);
* **Escalabilidade**  (volume de dados e tráfego);
* **Disponibilidade**  (tempo disponível, tempo indisponível, 24x7, 99,9%);
* **Segurança**  (autenticação, autorização, confidencialidade dos dados);
* **Extensibilidade**  (novas funcionalidades, plugins);
* **Flexibilidade**  (capacidade de ser usado para coisas não previstas);
* **Auditoria**;
* **Monitoramento**;
* **Confiabilidade**;
* **Resiliência**  (failover/disaster recovery, manual vs automatic);
* **Interoperabilidade**;
* **I18n e L10n**;
* **Acessibilidade**;
* **Usabilidade**;


Restrições
----------

**Pendente**

* **Prazo**;
* **Orçamento**;
* **Tamanho da equipe de desenvolvimento**;
* **Plataformas de implantação**: Ubuntu, CentOS, contêineres Docker, Windows(?);
* **Hardware**;
* **Integração com sistemas pré-existentes**: OPAC, OPAC-PROC, ArticleMeta;
* **Tecnologias de IPC**: gRPC, Apache Thrift, Restful API;
* **Licenciamento**: preferencialmente BSD 2-clause, mas outras licenças livres
  poderão ser avaliadas;


