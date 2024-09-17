if (!require(RSQLite)) {
    install.packages("RSQLite", dependencies = TRUE)
    install.packages("ggplot2", dependencies = TRUE)
}

library(RSQLite)
library(ggplot2)

con <- dbConnect(RSQLite::SQLite(), dbname = "fiap-agro.db")

query <- "SELECT * FROM planting_data"
data <- dbGetQuery(con, query)

data$efficiency <- data$input_amount / data$usable_area  # Eficiência = litros por m²

ggplot(data, aes(x = shape, y = efficiency, fill = shape)) +
    geom_boxplot(outlier.color = "red", outlier.shape = 8) +
    labs(title = "Eficiência de Uso de Insumos por Forma Geométrica", 
         x = "Forma Geométrica", y = "Eficiência (Litros/m²)") +
    theme_minimal() +
    scale_fill_brewer(palette = "Pastel2")

ggplot(data, aes(x = usable_area)) +
    geom_histogram(binwidth = 10000, fill = "lightblue", color = "black") +
    labs(title = "Distribuição de Áreas Usáveis", x = "Área Usável (m²)", y = "Frequência") +
    theme_minimal()


# Função para calcular estatísticas básicas
calc_stats <- function(column) {
  mean_value <- mean(column, na.rm = TRUE)
  median_value <- median(column, na.rm = TRUE)
  sd_value <- sd(column, na.rm = TRUE)
  return(list(mean = mean_value, median = median_value, sd = sd_value))
}

# Calcular estatísticas para total_area, usable_area, input_amount
total_area_stats <- calc_stats(data$total_area)
usable_area_stats <- calc_stats(data$usable_area)
input_amount_stats <- calc_stats(data$input_amount)

# Exibir os resultados
cat("== Estatísticas para AREA TOTAL ==\n")
cat("Média:", total_area_stats$mean, "\n")
cat("Mediana:", total_area_stats$median, "\n")
cat("Desvio Padrão:", total_area_stats$sd, "\n\n")

cat("== Estatísticas para AREA UTIL ==\n")
cat("Média:", usable_area_stats$mean, "\n")
cat("Mediana:", usable_area_stats$median, "\n")
cat("Desvio Padrão:", usable_area_stats$sd, "\n\n")

cat("== Estatísticas para QUANTIDADE DE INSUMO ==\n")
cat("Média:", input_amount_stats$mean, "\n")
cat("Mediana:", input_amount_stats$median, "\n")
cat("Desvio Padrão:", input_amount_stats$sd, "\n")

# Fechar a conexão com o banco de dados
dbDisconnect(con)
