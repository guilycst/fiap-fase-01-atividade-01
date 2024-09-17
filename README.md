Aqui está uma versão otimizada e mais agradável do README.md, com foco nos resultados e funcionalidades entregues no projeto:

---

# FarmTech Solutions - Aplicativo para Gestão de Agricultura Digital

## Visão Geral

Este projeto foi desenvolvido pela equipe **FarmTech Solutions** para atender uma fazenda que investe em **Agricultura Digital**. O objetivo principal foi criar uma aplicação em **Python** e **R** que oferece cálculos relacionados a áreas de plantio, manejo de insumos e análise estatística, além de uma ferramenta para consulta climática.

O projeto está organizado em duas partes principais: a aplicação desenvolvida em **Python**, que gerencia os dados relacionados ao plantio e insumos, e a análise dos dados com **R**, gerando estatísticas e gráficos. Além disso, criamos um script em **R** que faz a consulta climática de cidades usando a API do OpenWeather.

## Funcionalidades

### Aplicação em Python

1. **Gerenciamento de Dados de Plantio**:
   - **Inserção de Dados**: Permite adicionar informações sobre culturas, área de plantio e quantidade de insumos utilizados.
   - **Cálculo Automático de Área e Insumos**: Baseado em diferentes formas geométricas e nas dimensões informadas pelo usuário.
   - **Persistência em Banco de Dados SQLite**: Todos os dados são armazenados em um banco de dados local para análise posterior.
   - **Navegação Intuitiva**: Interação simplificada com o menu usando o mouse e/ou teclado para navegar, inserir, editar, consultar e deletar registros.

2. **Edição e Consulta de Registros**:
   - **Consulta de Registros**: Exibe os registros armazenados com a possibilidade de navegação por meio do mouse e/ou das setas.
   - **Edição**: Toque de tecla (**Enter** ou **e**), o usuário pode editar qualquer registro selecionado.
   - **Deleção**: Remova registros diretamente da tabela de consulta usando as teclas **d**, **delete** ou **backspace**.

### Análise Estatística em R

1. **Cálculos Estatísticos**:
   - O script `planting_data_stats.R` realiza uma análise detalhada dos dados de plantio e insumos armazenados no banco de dados SQLite.
   - **Métricas**: O script calcula a média, mediana e desvio padrão para áreas de plantio e quantidade de insumos, oferecendo uma visão clara da eficiência de cada cultura.

2. **Visualização de Dados**:
   - Geração de gráficos, como:
     - **Boxplots**: Exibem a eficiência do uso de insumos por diferentes formas geométricas.
     - **Histogramas**: Mostram a distribuição de áreas plantadas, ajudando a identificar padrões no uso do espaço.

### Consulta Climática em R

1. **Dados Climáticos em Tempo Real**:
   - O script `consulta_clima_R.R` permite consultar informações meteorológicas de qualquer cidade, fornecendo:
     - Temperatura
     - Umidade
     - Velocidade do vento
     - Pressão atmosférica
     - Percentual de nuvens
     - Coordenadas geográficas

2. **Conectividade com a API OpenWeather**:
   - O usuário precisa apenas inserir o nome da cidade e o script retornará as informações climáticas atuais.
   - A configuração é simples, exigindo apenas uma chave de API do OpenWeather, que pode ser facilmente configurada como uma variável de ambiente (export OPENWEATHER_API_KEY=...).

## Estrutura do Projeto

```
/my_program
│
├── main.py                # Controla o fluxo e a interface usando PyTerm GUI
├── requirements.txt       # Dependências do app python
├── persistence.py         # Persistência no banco de dados SQLite
├── metadata.json          # Define culturas, formatos e insumos a serem renderizados pelo app
├── fiap-agro.db           # Banco de dados SQLite para manter os dados gerados para análise (R)
├── planting_data_stats.R  # Script R para calcular estatísticas e gerar gráficos
├── consulta_clima_R.R     # Script R para consultar dados climáticos da API OpenWeather
├── style.css              # CSS especifico da biblioteca Textual que gera a TUI
├── resumo.pdf             # Resumo do artigo acadêmico
├── video_link.txt         # Link para o vídeo no YouTube (não listado)
├── /assets                # Documentação sobre insumos agrícolas (.pdf)
```

## Como Usar

### Python

1. **Iniciar Aplicação**:
   - Criar e ativar ambiente virtual python
   - Instalar as dependências do arquivo requirements.txt
   - Execute o arquivo `main.py` para acessar o menu principal.
   - Use o mouse e/ou as setas para navegar e **Enter** para selecionar uma opção.
   - Insira dados sobre o plantio e insumos conforme solicitado.

2. **Edição e Consulta**:
   - Navegue pelos registros salvos com o mouse e/ou as setas e edite-os pressionando **Enter** ou **e**.
   - Para deletar, utilize as teclas **d**, **delete** ou **backspace**.

### R

1. **Análise Estatística**:
   - Execute o script `planting_data_stats.R` para calcular estatísticas e visualizar gráficos a partir dos dados inseridos na aplicação Python.

2. **Consulta Climática**:
   - Execute o script `consulta_clima_R.R`, insira o nome da cidade desejada e obtenha os dados climáticos em tempo real.
   - Certifique-se de que a variável de ambiente `OPENWEATHER_API_KEY` esteja configurada corretamente.

## Detalhes da Entrega

- **Resumos Acadêmicos**: O artigo acadêmico requerido pela disciplina de **Formação Social** foi resumido e está disponível em **resumo.pdf**.
- **Demonstração em Vídeo**: Um vídeo demonstrando a execução completa da aplicação foi gravado e está disponível no **YouTube**. O link para o vídeo está incluído no arquivo `video_link.txt`.


