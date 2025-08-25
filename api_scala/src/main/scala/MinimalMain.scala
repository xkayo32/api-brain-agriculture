import akka.actor.typed.ActorSystem
import akka.actor.typed.scaladsl.Behaviors
import akka.http.scaladsl.Http
import akka.http.scaladsl.model._
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.Route
import de.heikoseeberger.akkahttpcirce.FailFastCirceSupport._
import io.circe.generic.auto._
import models._
import scala.util.{Failure, Success}
import scala.concurrent.{ExecutionContext, Future}
import scala.io.StdIn
import java.time.LocalDateTime
import scala.collection.mutable
import java.util.Base64

object MinimalMain {
  
  case class LoginRequest(username: String, password: String)
  case class LoginResponse(access_token: String, token_type: String = "bearer")
  
  // Validador de documento simples
  object DocumentValidator {
    def isValid(document: String): Boolean = {
      val cleanDoc = document.replaceAll("[^0-9]", "")
      cleanDoc.length == 11 || cleanDoc.length == 14 // CPF ou CNPJ
    }
  }
  
  // Gerador de token simples
  object SecurityUtils {
    def generateToken(username: String): String = {
      val payload = s"""{"sub":"$username","iat":${System.currentTimeMillis()/1000},"exp":${System.currentTimeMillis()/1000 + 3600}}"""
      Base64.getEncoder.encodeToString(payload.getBytes)
    }
  }
  
  // Documentação OpenAPI em JSON
  val openApiSpec = """{
    "openapi": "3.0.0",
    "info": {
      "title": "Brain Agriculture API",
      "version": "1.0.0",
      "description": "API para gerenciamento de produtores rurais - Sistema Brain Agriculture"
    },
    "servers": [
      {
        "url": "http://localhost:8081",
        "description": "Servidor de desenvolvimento"
      }
    ],
    "paths": {
      "/health": {
        "get": {
          "summary": "Health Check",
          "description": "Verifica se a API está funcionando",
          "responses": {
            "200": {
              "description": "API funcionando",
              "content": {
                "text/plain": {
                  "schema": {
                    "type": "string",
                    "example": "🌾 API Scala funcionando!"
                  }
                }
              }
            }
          }
        }
      },
      "/api/auth/login": {
        "post": {
          "summary": "Fazer login",
          "description": "Autentica usuário e retorna token JWT",
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "username": {"type": "string", "example": "admin"},
                    "password": {"type": "string", "example": "admin123"}
                  }
                }
              }
            }
          },
          "responses": {
            "200": {
              "description": "Login realizado com sucesso",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "access_token": {"type": "string"},
                      "token_type": {"type": "string", "example": "bearer"}
                    }
                  }
                }
              }
            },
            "401": {
              "description": "Credenciais inválidas"
            }
          }
        }
      },
      "/api/producers": {
        "get": {
          "summary": "Listar produtores",
          "description": "Retorna lista de todos os produtores cadastrados",
          "responses": {
            "200": {
              "description": "Lista de produtores",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "id": {"type": "integer"},
                        "document": {"type": "string"},
                        "name": {"type": "string"},
                        "createdAt": {"type": "string", "format": "date-time"},
                        "updatedAt": {"type": "string", "format": "date-time"}
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "post": {
          "summary": "Criar produtor",
          "description": "Cria um novo produtor rural",
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "document": {"type": "string", "example": "12345678901", "description": "CPF (11 dígitos) ou CNPJ (14 dígitos)"},
                    "name": {"type": "string", "example": "João Silva"}
                  }
                }
              }
            }
          },
          "responses": {
            "201": {
              "description": "Produtor criado com sucesso",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "id": {"type": "integer"},
                      "document": {"type": "string"},
                      "name": {"type": "string"},
                      "createdAt": {"type": "string", "format": "date-time"},
                      "updatedAt": {"type": "string", "format": "date-time"}
                    }
                  }
                }
              }
            },
            "400": {
              "description": "Documento inválido"
            }
          }
        }
      },
      "/api/producers/{id}": {
        "get": {
          "summary": "Buscar produtor por ID",
          "description": "Retorna um produtor específico pelo ID",
          "parameters": [
            {
              "name": "id",
              "in": "path",
              "required": true,
              "schema": {"type": "integer"},
              "description": "ID do produtor"
            }
          ],
          "responses": {
            "200": {
              "description": "Produtor encontrado",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "id": {"type": "integer"},
                      "document": {"type": "string"},
                      "name": {"type": "string"},
                      "createdAt": {"type": "string", "format": "date-time"},
                      "updatedAt": {"type": "string", "format": "date-time"}
                    }
                  }
                }
              }
            },
            "404": {
              "description": "Produtor não encontrado"
            }
          }
        },
        "delete": {
          "summary": "Deletar produtor",
          "description": "Remove um produtor do sistema",
          "parameters": [
            {
              "name": "id",
              "in": "path",
              "required": true,
              "schema": {"type": "integer"},
              "description": "ID do produtor"
            }
          ],
          "responses": {
            "204": {
              "description": "Produtor deletado com sucesso"
            },
            "404": {
              "description": "Produtor não encontrado"
            }
          }
        }
      },
      "/api/dashboard/summary": {
        "get": {
          "summary": "Dashboard - Resumo",
          "description": "Retorna estatísticas resumidas do sistema",
          "responses": {
            "200": {
              "description": "Estatísticas do dashboard",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "total_producers": {"type": "integer"},
                      "total_farms": {"type": "integer"},
                      "total_area": {"type": "integer"}
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }"""
  
  def main(args: Array[String]): Unit = {
    // Sistema de atores
    implicit val system = ActorSystem(Behaviors.empty, "brain-agriculture-system")
    implicit val ec: ExecutionContext = system.executionContext

    // Repositório em memória
    val producers = mutable.Map[Int, Producer]()
    var nextId = 1

    // Rotas da API
    val routes: Route = concat(
      // Documentação OpenAPI
      path("openapi.json") {
        get {
          complete(HttpResponse(
            StatusCodes.OK,
            entity = HttpEntity(ContentTypes.`application/json`, openApiSpec)
          ))
        }
      },
      
      // Swagger UI - link para visualizar a documentação
      path("docs") {
        get {
          val swaggerHtml = s"""
            <!DOCTYPE html>
            <html>
            <head>
              <title>Brain Agriculture API - Documentação</title>
              <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .method { font-weight: bold; color: #007bff; }
                .url { font-family: monospace; background: #e9ecef; padding: 3px 6px; border-radius: 3px; }
                pre { background: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; }
              </style>
            </head>
            <body>
              <div class="container">
                <h1>🌾 Brain Agriculture API - Documentação</h1>
                <p>API para gerenciamento de produtores rurais</p>
                
                <h2>📋 Endpoints Disponíveis</h2>
                
                <div class="endpoint">
                  <h3><span class="method">GET</span> Health Check</h3>
                  <p><span class="url">GET /health</span></p>
                  <p>Verifica se a API está funcionando</p>
                </div>
                
                <div class="endpoint">
                  <h3><span class="method">POST</span> Login</h3>
                  <p><span class="url">POST /api/auth/login</span></p>
                  <p>Autentica usuário (admin/admin123) e retorna token JWT</p>
                  <pre>{
  "username": "admin",
  "password": "admin123"
}</pre>
                </div>
                
                <div class="endpoint">
                  <h3><span class="method">GET</span> Listar Produtores</h3>
                  <p><span class="url">GET /api/producers</span></p>
                  <p>Retorna lista de todos os produtores cadastrados</p>
                </div>
                
                <div class="endpoint">
                  <h3><span class="method">POST</span> Criar Produtor</h3>
                  <p><span class="url">POST /api/producers</span></p>
                  <p>Cria um novo produtor rural</p>
                  <pre>{
  "document": "12345678901",
  "name": "João Silva"
}</pre>
                </div>
                
                <div class="endpoint">
                  <h3><span class="method">GET</span> Buscar Produtor</h3>
                  <p><span class="url">GET /api/producers/{id}</span></p>
                  <p>Retorna um produtor específico pelo ID</p>
                </div>
                
                <div class="endpoint">
                  <h3><span class="method">DELETE</span> Deletar Produtor</h3>
                  <p><span class="url">DELETE /api/producers/{id}</span></p>
                  <p>Remove um produtor do sistema</p>
                </div>
                
                <div class="endpoint">
                  <h3><span class="method">GET</span> Dashboard</h3>
                  <p><span class="url">GET /api/dashboard/summary</span></p>
                  <p>Retorna estatísticas resumidas do sistema</p>
                </div>
                
                <h2>🔗 Links Úteis</h2>
                <ul>
                  <li><a href="/openapi.json">OpenAPI JSON Specification</a></li>
                  <li><a href="https://petstore.swagger.io/?url=http://localhost:8081/openapi.json" target="_blank">Swagger UI (Petstore)</a></li>
                </ul>
                
                <h2>🚀 Como Testar</h2>
                <p>Use curl ou Postman para testar os endpoints:</p>
                <pre>curl -X GET http://localhost:8081/health
curl -X POST http://localhost:8081/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "admin", "password": "admin123"}'</pre>
              </div>
            </body>
            </html>
          """
          complete(HttpResponse(
            StatusCodes.OK,
            entity = HttpEntity(ContentTypes.`text/html(UTF-8)`, swaggerHtml)
          ))
        }
      },
      
      // Health check
      pathPrefix("health") {
        get {
          complete(HttpResponse(StatusCodes.OK, entity = "🌾 API Scala funcionando!"))
        }
      },
      
      // Auth
      pathPrefix("api" / "auth") {
        path("login") {
          post {
            entity(as[LoginRequest]) { loginRequest =>
              if (loginRequest.username == "admin" && loginRequest.password == "admin123") {
                val token = SecurityUtils.generateToken(loginRequest.username)
                complete(StatusCodes.OK, LoginResponse(token))
              } else {
                complete(StatusCodes.Unauthorized, Map("error" -> "Credenciais inválidas"))
              }
            }
          }
        }
      },
      
      // Producers
      pathPrefix("api" / "producers") {
        concat(
          // GET /api/producers - listar
          pathEnd {
            get {
              complete(StatusCodes.OK, producers.values.toList)
            }
          },
          
          // POST /api/producers - criar
          pathEnd {
            post {
              entity(as[CreateProducerRequest]) { request =>
                if (DocumentValidator.isValid(request.document)) {
                  val producer = Producer(
                    id = Some(nextId),
                    document = request.document,
                    name = request.name
                  )
                  producers(nextId) = producer
                  nextId += 1
                  complete(StatusCodes.Created, producer)
                } else {
                  complete(StatusCodes.BadRequest, Map("error" -> "Documento inválido"))
                }
              }
            }
          },
          
          // GET /api/producers/{id}
          path(IntNumber) { id =>
            get {
              producers.get(id) match {
                case Some(producer) => complete(StatusCodes.OK, producer)
                case None => complete(StatusCodes.NotFound, Map("error" -> "Produtor não encontrado"))
              }
            }
          },
          
          // DELETE /api/producers/{id}  
          path(IntNumber) { id =>
            delete {
              if (producers.remove(id).isDefined) {
                complete(StatusCodes.NoContent)
              } else {
                complete(StatusCodes.NotFound, Map("error" -> "Produtor não encontrado"))
              }
            }
          }
        )
      },
      
      // Dashboard
      pathPrefix("api" / "dashboard") {
        path("summary") {
          get {
            val totalProducers = producers.size
            val summary = Map(
              "total_producers" -> totalProducers,
              "total_farms" -> 0,
              "total_area" -> 0
            )
            complete(StatusCodes.OK, summary)
          }
        }
      }
    )

    // Configurações do servidor
    val host = "0.0.0.0"
    val port = 8080

    // Iniciar servidor
    val bindingFuture = Http().newServerAt(host, port).bind(routes)

    bindingFuture.onComplete {
      case Success(binding) =>
        val address = binding.localAddress
        println(s"🌾 Brain Agriculture - API Scala FUNCIONANDO!")
        println(s"✅ Servidor: http://${address.getHostString}:${address.getPort}/")
        println(s"📋 Health: http://${address.getHostString}:${address.getPort}/health")
        println(s"🔒 Login: POST http://${address.getHostString}:${address.getPort}/api/auth/login")
        println(s"👨‍🌾 Producers: http://${address.getHostString}:${address.getPort}/api/producers")
        println(s"📊 Dashboard: http://${address.getHostString}:${address.getPort}/api/dashboard/summary")
        println("=" * 60)
        println("Credenciais: admin / admin123")
        println("Pressione ENTER para parar...")

      case Failure(ex) =>
        println(s"❌ Falha ao iniciar servidor: ${ex.getMessage}")
        system.terminate()
    }

    // Manter servidor rodando
    scala.concurrent.Await.result(system.whenTerminated, scala.concurrent.duration.Duration.Inf)
  }
}