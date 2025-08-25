FROM openjdk:11-jdk

# Instalar SBT
RUN apt-get update && \
    apt-get install -y curl && \
    curl -L https://github.com/sbt/sbt/releases/download/v1.9.7/sbt-1.9.7.tgz | tar -xz -C /opt && \
    ln -s /opt/sbt/bin/sbt /usr/local/bin/sbt && \
    apt-get clean

# Diretorio de trabalho
WORKDIR /app

# Copiar arquivos de build
COPY build.sbt .
COPY project ./project

# Baixar dependencias
RUN sbt update

# Copiar codigo fonte
COPY src ./src

# Compilar aplicacao
RUN sbt compile

# Expor porta
EXPOSE 8080

# Comando para rodar MinimalMain
CMD ["sbt", "runMain MinimalMain"]