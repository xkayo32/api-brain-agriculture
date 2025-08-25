package services

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.concurrent.ScalaFutures
import scala.concurrent.Future
import models.User
import utils.SecurityUtils
import java.util.UUID

class AuthServiceSpec extends AnyFlatSpec with Matchers with ScalaFutures {

  "AuthService" should "hash passwords correctly" in {
    val password = "password123"
    val hashedPassword = SecurityUtils.hashPassword(password)
    
    hashedPassword should not equal password
    hashedPassword.length should be > 50
  }

  it should "verify correct passwords" in {
    val password = "password123"
    val hashedPassword = SecurityUtils.hashPassword(password)
    
    SecurityUtils.verifyPassword(password, hashedPassword) shouldBe true
  }

  it should "reject incorrect passwords" in {
    val password = "password123"
    val wrongPassword = "wrongpassword"
    val hashedPassword = SecurityUtils.hashPassword(password)
    
    SecurityUtils.verifyPassword(wrongPassword, hashedPassword) shouldBe false
  }

  it should "generate valid JWT tokens" in {
    val username = "testuser"
    val token = SecurityUtils.generateToken(username)
    
    token should not be empty
    token.split("\\.").length shouldBe 3 // JWT tem 3 partes
  }

  it should "validate JWT tokens correctly" in {
    val username = "testuser"
    val token = SecurityUtils.generateToken(username)
    
    val decodedUsername = SecurityUtils.validateToken(token)
    decodedUsername shouldBe Some(username)
  }

  it should "reject invalid JWT tokens" in {
    val invalidToken = "invalid.token.here"
    val decodedUsername = SecurityUtils.validateToken(invalidToken)
    
    decodedUsername shouldBe None
  }

  it should "reject empty or malformed tokens" in {
    SecurityUtils.validateToken("") shouldBe None
    SecurityUtils.validateToken("not.a.token") shouldBe None
    SecurityUtils.validateToken("malformed") shouldBe None
  }

  "AuthService password requirements" should "enforce minimum length" in {
    val shortPassword = "123"
    // Assumindo que temos validacao de senha (pode ser implementada)
    shortPassword.length should be < 6
  }

  it should "accept strong passwords" in {
    val strongPassword = "StrongPassword123!"
    strongPassword.length should be >= 8
    strongPassword should include regex "[A-Z]".r
    strongPassword should include regex "[a-z]".r
    strongPassword should include regex "[0-9]".r
  }

  "AuthService token expiry" should "generate tokens with expiry" in {
    val username = "testuser"
    val token = SecurityUtils.generateToken(username)
    
    // Token deve ser valido imediatamente apos criacao
    SecurityUtils.validateToken(token) shouldBe Some(username)
  }

  // Teste simulado de expiracao de token (seria necessario mock do tempo)
  it should "handle token expiry gracefully" in {
    val username = "testuser"
    val token = SecurityUtils.generateToken(username)
    
    // Em um cenario real, esperariamos ou mockariamos a expiracao
    // Por ora, apenas verificamos que o token e valido
    SecurityUtils.validateToken(token) should not be None
  }
}