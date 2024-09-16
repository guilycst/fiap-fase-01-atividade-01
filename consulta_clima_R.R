library(httr)
library(jsonlite)
city <- readline(prompt = "Digite o nome da cidade: ")
if (trimws(city) == "") {
  cat("Erro: Nenhum nome de cidade fornecido.\n")
  quit(save = "no")
}
api_key <- Sys.getenv("OPENWEATHER_API_KEY")
if (api_key == "") {
  cat("Erro: A chave da API não está definida. Defina a variável de ambiente OPENWEATHER_API_KEY.\n")
  quit(save = "no")
}

url <- paste0("http://api.openweathermap.org/data/2.5/weather?q=", URLencode(city), "&appid=", api_key, "&units=metric")
response <- GET(url)

cat("Código de status da resposta:", status_code(response), "\n")


data <- fromJSON(content(response, "text"))
if (status_code(response) == 200) {
  temperatura <- data$main$temp
  umidade <- data$main$humidity
  vento <- data$wind$speed
  pressao <- data$main$pressure
  nuvens <- data$clouds$all
  coordenadas <- paste(data$coord$lat, data$coord$lon, sep=", ")
  atualizacao <- as.POSIXct(data$dt, origin="1970-01-01", tz="UTC")
  timezone <- data$timezone
  
  cat("Clima em", city, ":\n")
  cat("Temperatura:", temperatura, "°C\n")
  cat("Umidade:", umidade, "%\n")
  cat("Velocidade do vento:", vento, "m/s\n")
  cat("Pressão atmosférica:", pressao, "hPa\n")
  cat("Nuvens:", nuvens, "%\n")
  cat("Coordenadas (Lat, Lon):", coordenadas, "\n")
  cat("Data e hora da última atualização:", atualizacao, "\n")
  cat("Fuso horário:", timezone, "\n")
} else {
  error_message <- content(response, "text")
  cat("Mensagem de erro da API:", error_message, "\n")
}