import utils.DocumentValidator
import utils.SecurityUtils

/**
 * Sistema de testes customizado para API Scala
 */
object TestRunner {

  def main(args: Array[String]): Unit = {
    println("SISTEMA DE TESTES DA API BRAIN AGRICULTURE - SCALA")
    println("=" * 55)
    
    runValidatorTests()
    runSecurityTests()
    runModelTests()
    
    println("\n" + "=" * 55)
    println("RESUMO DOS TESTES SCALA CONCLUIDO")
    println("=" * 55)
  }

  def runValidatorTests(): Unit = {
    println("\n=== EXECUTANDO TESTES DOS VALIDADORES ===")
    
    try {
      // Testes de CPF
      assert(DocumentValidator.validateCPF("11144477735"), "CPF válido deveria passar")
      assert(DocumentValidator.validateCPF("111.444.777-35"), "CPF formatado deveria passar")
      assert(!DocumentValidator.validateCPF("11144477736"), "CPF inválido deveria falhar")
      assert(!DocumentValidator.validateCPF("11111111111"), "CPF com dígitos iguais deveria falhar")
      println("OK: Testes de validação CPF passaram")

      // Testes de CNPJ
      assert(DocumentValidator.validateCNPJ("11222333000181"), "CNPJ válido deveria passar")
      assert(DocumentValidator.validateCNPJ("11.222.333/0001-81"), "CNPJ formatado deveria passar")
      assert(!DocumentValidator.validateCNPJ("11222333000192"), "CNPJ inválido deveria falhar")
      assert(!DocumentValidator.validateCNPJ("11111111111111"), "CNPJ com dígitos iguais deveria falhar")
      println("OK: Testes de validação CNPJ passaram")

      println("OK: Testes de validação básica passaram")

      println("Todos os testes de validadores passaram!")
    } catch {
      case e: AssertionError => 
        println(s"ERRO: Teste de validador falhou: ${e.getMessage}")
      case e: Exception => 
        println(s"ERRO: Erro durante testes de validadores: ${e.getMessage}")
    }
  }

  def runSecurityTests(): Unit = {
    println("\n=== EXECUTANDO TESTES DE SEGURANÇA ===")
    
    try {
      val password = "password123"
      val hashedPassword = SecurityUtils.hashPassword(password)
      
      // Teste de hash
      assert(hashedPassword != password, "Hash deve ser diferente da senha original")
      assert(hashedPassword.length > 50, "Hash deve ter tamanho adequado")
      println("OK: Hash de senha funcionando")
      
      // Teste de verificação
      assert(SecurityUtils.checkPassword(password, hashedPassword), "Verificação de senha correta")
      assert(!SecurityUtils.checkPassword("wrongpassword", hashedPassword), "Rejeição de senha errada")
      println("OK: Verificação de senha funcionando")
      
      // Teste de JWT
      val username = "testuser"
      val token = SecurityUtils.generateToken(username)
      assert(token.nonEmpty, "Token não deve estar vazio")
      assert(token.split("\\.").length == 3, "Token JWT deve ter 3 partes")
      println("OK: Geração de token JWT funcionando")
      
      val decodedUsername = SecurityUtils.validateToken(token)
      assert(decodedUsername.contains(username), "Validação de token deve retornar username")
      println("OK: Validação de token JWT funcionando")
      
      // Teste de token inválido
      val invalidResult = SecurityUtils.validateToken("invalid.token.here")
      assert(invalidResult.isEmpty, "Token inválido deve ser rejeitado")
      println("OK: Rejeição de token inválido funcionando")
      
      println("Todos os testes de segurança passaram!")
    } catch {
      case e: AssertionError => 
        println(s"ERRO: Teste de segurança falhou: ${e.getMessage}")
      case e: Exception => 
        println(s"ERRO: Erro durante testes de segurança: ${e.getMessage}")
    }
  }

  def runModelTests(): Unit = {
    println("\n=== EXECUTANDO TESTES BÁSICOS DE MODELOS ===")
    
    try {
      import models._
      import java.util.UUID
      
      // Teste básico de Producer
      val producer = Producer(
        document = "12345678909",
        name = "João Silva"
      )
      
      assert(producer.name == "João Silva", "Nome do producer deve estar correto")
      assert(producer.document == "12345678909", "Documento deve estar correto")
      println("OK: Modelo Producer funcionando")
      
      println("Todos os testes básicos de modelos passaram!")
    } catch {
      case e: AssertionError => 
        println(s"ERRO: Teste de modelo falhou: ${e.getMessage}")
      case e: Exception => 
        println(s"ERRO: Erro durante testes de modelos: ${e.getMessage}")
        e.printStackTrace()
    }
  }
}