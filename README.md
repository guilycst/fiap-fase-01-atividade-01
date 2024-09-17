# FIAP - Fase 01 - Atividade 01

## Iniciando os Trabalhos da Startup

### Atenção: Atividade Avaliativa

- Verifique se o arquivo do upload está correto, pois não é possível enviar um outro arquivo após o fechamento da entrega na plataforma ou correção do professor.
- Não deixe para realizar a entrega da atividade nos últimos minutos do prazo. Você pode ter algum problema e perder a entrega. As entregas são realizadas apenas pela plataforma.
- Não disponibilize a resposta da sua atividade em grupos de WhatsApp, Discord, Microsoft Teams, pois pode gerar plágio e zerar a atividade para todos.
- Você tem um período máximo de 15 dias após a publicação da nota para solicitar a revisão da correção.

## Introdução

Você e seu grupo estão na **Startup FarmTech Solutions**, trabalhando na equipe de Dev. Vocês podem usar o **ChatGPT**, **Germini** ou outra Inteligência Artificial (IA) de sua escolha para ajudar com essa tarefa. A **FIAP** não condena o uso de IAs, desde que o aluno tenha o olhar crítico para filtrar erros e acertos das respostas propostas por elas.

A **FarmTech Solutions** fechou um contrato com uma fazenda que investe em inovação e tecnologia para aumentar sua produtividade e pretende migrar para a **Agricultura Digital**. Para atender esse importante cliente, a **FarmTech** desenvolverá uma aplicação em **Python** que deve incluir:

a. Suporte para 2 tipos de culturas. O grupo deve decidir quais culturas trabalhar, considerando as principais culturas de seu estado.

b. Cálculo de área de plantio para cada cultura. O grupo decide qual tipo de figura geométrica calcular como área plantada para cada tipo de cultura.

c. Cálculo do manejo de insumos. O grupo escolhe o tipo de cultura, o produto e a quantidade necessária, como, por exemplo, aplicar fosfato no café e pulverizar 500 mL/metro com o trator. Quantas ruas a lavoura tem? Quantos litros serão necessários?

d. Os dados devem estar organizados em vetores.

e. A aplicação em **Python** precisa ter um menu de opções para:
   - Entrada de dados (para realizar os cálculos);
   - Saída de dados (impressões no terminal);
   - Atualização de dados em qualquer posição do vetor;
   - Deleção de dados do vetor;
   - Opção "sair do programa".

f. Usar rotinas de loop e decisão.

g. Em seguida, usar esses dados para desenvolver uma aplicação em **R** que calcule dados estatísticos básicos, como média e desvio. O projeto deve ser versionado no **GitHub**, trabalhando em equipe para simular um ambiente colaborativo de desenvolvimento.

h. Na disciplina de **Formação Social**, o grupo deve resumir o artigo disponível no Google Acadêmico ([link aqui](https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1003485/1/CAP8.pdf)). O resumo deve ter até 1 folha A4, letra Arial 11, espaçamento 1 entre linhas, com margens direita e esquerda de 2 cm.

### Ir Além

Usando **R** (e não **Python**), conecte-se a uma **API meteorológica pública** para coletar dados climáticos, processar e exibir as informações via texto simples no terminal.

## O Que Precisa Entregar?

Compacte todos os arquivos em um único **arquivo ZIP**: **Python**, **R**, o **resumo do artigo** e o **link do vídeo no YouTube**. Além disso, grave um vídeo simples, de até 5 minutos, usando seu celular ou um gravador de tela simples (por exemplo, **streamyard.com**), mostrando a tela do seu computador para comprovar o funcionamento completo da sua aplicação em Python e R. Poste o vídeo no **YouTube** como “não listado” e adicione o link a um arquivo TXT dentro do pacote ZIP.

## Estrutura do projeto

```
/my_program
│
├── main.py              # Controla o fluxo e a interface usando PyTerm GUI
├── persistence.py       # Persistência no banco de dados SQLite
├── metadata.json        # Define culturas, formatos e insumos a serem renderizados pelo app
├── style.css            # CSS especifico da biblioteca Textual que gera a TUI
├── fiap-agro.db         # Banco de dados SQLite para manter os dados gerados para analise (R)
├── /assets              # Documentação sobre insumos agrícolas (.pdf)
```

## Como Interagir com o Aplicativo Usando o Teclado

Este aplicativo permite a interação por meio do teclado para facilitar a navegação e operação. A seguir, estão as principais combinações de teclas que você pode utilizar:

### Menu Principal
- **Setas**: Navegar pelas opções do menu.
- **Enter**: Selecionar a opção destacada.
- **Escape**: Sair do aplicativo.

### Inserção de Novos Dados
- **Enter**: Selecionar uma cultura ou forma geométrica durante o processo de inserção de dados.
- **Tab**: Navegar pelos campos de inserção de dados.
- **Shift + Tab**: Navegar pelos campos de inserção de dados na ordem inversa.
- **Enter**: Confirmar e prosseguir para o próximo passo.
- **Escape**: Cancelar o processo de inserção de dados e voltar ao menu anterior.

### Consulta de Dados
- **Setas**: Navegar pelos registros exibidos na tabela de consulta.
- **Enter** ou **e**: Editar o registro selecionado.
- **d**, **delete** ou **backspace**: Deletar o registro selecionado.
- **Escape**: Voltar ao menu anterior.

### Edição de Dados
- **Tab**: Navegar pelos campos de edição.
- **Shift + Tab**: Navegar pelos campos de edição na ordem inversa.
- **Enter**: Confirmar a atualização dos dados.
- **Escape**: Cancelar a edição e voltar à tabela de consulta.

### Ajuda e Comandos Gerais
- **Escape**: Voltar ou sair da tela atual.
- **Enter**: Confirmar a ação selecionada.

## Referencias

https://www.agro.bayer.com.br/produtos-protecao-cultivos?p=1

http://www.iea.agricultura.sp.gov.br/out/TerTexto.php?codTexto=16198#:~:text=O%20levantamento%20final%20da%20safra,rela%C3%A7%C3%A3o%20%C3%A0%20safra%202021%2F22.

## Links externos avaliação

**App python demo:**
https://youtu.be/4s-nyn-sgfo
