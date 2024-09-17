# Instalar o pacote necessário, caso ainda não tenha
if (!require(RSQLite)) {
    install.packages("RSQLite", dependencies = TRUE)
    install.packages("ggplot2", dependencies = TRUE)
}

# Carregar as bibliotecas
library(RSQLite)
library(ggplot2)

# Conectar ao banco de dados SQLite
con <- dbConnect(RSQLite::SQLite(), dbname = "fiap-agro.db")

# Ler dados da tabela
query <- "SELECT * FROM planting_data"
data <- dbGetQuery(con, query)

# Calcular a média e o desvio padrão para os campos total_area e input_amount
total_area_mean <- mean(data$total_area, na.rm = TRUE)
total_area_sd <- sd(data$total_area, na.rm = TRUE)

input_amount_mean <- mean(data$input_amount, na.rm = TRUE)
input_amount_sd <- sd(data$input_amount, na.rm = TRUE)

# Calcular a mediana
total_area_median <- median(data$total_area, na.rm = TRUE)
input_amount_median <- median(data$input_amount, na.rm = TRUE)

# Função para calcular a moda
mode_function <- function(x) {
    ux <- unique(x)
    ux[which.max(tabulate(match(x, ux)))]
}

# Calcular a moda
total_area_mode <- mode_function(data$total_area)
input_amount_mode <- mode_function(data$input_amount)

# Calcular o mínimo e máximo
total_area_min <- min(data$total_area, na.rm = TRUE)
total_area_max <- max(data$total_area, na.rm = TRUE)

input_amount_min <- min(data$input_amount, na.rm = TRUE)
input_amount_max <- max(data$input_amount, na.rm = TRUE)

# Calcular os quartis
total_area_quantiles <- quantile(data$total_area, na.rm = TRUE)
input_amount_quantiles <- quantile(data$input_amount, na.rm = TRUE)

# Exibir os resultados
cat("== Total Area ==\n")
cat("Média:", total_area_mean, "\n")
cat("Desvio Padrão:", total_area_sd, "\n")
cat("Mediana:", total_area_median, "\n")
cat("Moda:", total_area_mode, "\n")
cat("Mínimo:", total_area_min, "\n")
cat("Máximo:", total_area_max, "\n")
cat("Quartis:", total_area_quantiles, "\n\n")

cat("== Input Amount ==\n")
cat("Média:", input_amount_mean, "\n")
cat("Desvio Padrão:", input_amount_sd, "\n")
cat("Mediana:", input_amount_median, "\n")
cat("Moda:", input_amount_mode, "\n")
cat("Mínimo:", input_amount_min, "\n")
cat("Máximo:", input_amount_max, "\n")
cat("Quartis:", input_amount_quantiles, "\n")

# Criar o plot da relação entre área de manejo e área total
ggplot(data, aes(x = total_area, y = management_area)) +
    geom_point(color = "blue") +
    labs(title = "Relação entre Área de Manejo e Área Total", x = "Total Area", y = "Management Area") +
    theme_minimal()

# Criar o plot da comparação de formas geométricas em relação à área usável
ggplot(data, aes(x = shape, y = usable_area)) +
    geom_boxplot(fill = "lightblue") +
    labs(title = "Comparação entre Formas Geométricas de Plantio", x = "Shape", y = "Usable Area") +
    theme_minimal()

# Adicionar uma coluna de eficiência
data$efficiency <- data$usable_area / data$total_area

# Criar o plot da eficiência de uso da área
ggplot(data, aes(x = total_area, y = efficiency)) +
    geom_point(color = "green") +
    labs(title = "Eficiência de Uso da Área", x = "Total Area", y = "Efficiency (Usable/Total)") +
    theme_minimal()

# Criar o plot da relação entre área total e insumos
ggplot(data, aes(x = total_area, y = input_amount)) +
    geom_point(color = "red") +
    labs(title = "Relação entre Área Total e Insumos", x = "Total Area", y = "Input Amount") +
    theme_minimal()

# Fechar a conexão com o banco de dados
dbDisconnect(con)
