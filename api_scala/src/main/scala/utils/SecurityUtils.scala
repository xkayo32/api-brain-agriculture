package utils

import java.util.Base64
import java.security.SecureRandom
import scala.util.Try
import org.mindrot.jbcrypt.BCrypt

object SecurityUtils {
  
  private val random = new SecureRandom()
  
  def hashPassword(password: String): String = {
    BCrypt.hashpw(password, BCrypt.gensalt())
  }
  
  def checkPassword(password: String, hashedPassword: String): Boolean = {
    Try {
      BCrypt.checkpw(password, hashedPassword)
    }.getOrElse(false)
  }
  
  // Alias for tests
  def verifyPassword(password: String, hashedPassword: String): Boolean = {
    checkPassword(password, hashedPassword)
  }
  
  def generateToken(username: String): String = {
    val currentTime = System.currentTimeMillis() / 1000
    val expiration = currentTime + 3600 // 1 hour
    
    // Create JWT header
    val header = """{"alg":"HS256","typ":"JWT"}"""
    val encodedHeader = Base64.getEncoder.encodeToString(header.getBytes)
    
    // Create JWT payload
    val payload = s"""{"sub":"$username","iat":$currentTime,"exp":$expiration}"""
    val encodedPayload = Base64.getEncoder.encodeToString(payload.getBytes)
    
    // Create simple signature (in production would use proper HMAC)
    val signature = "signature"
    val encodedSignature = Base64.getEncoder.encodeToString(signature.getBytes)
    
    s"$encodedHeader.$encodedPayload.$encodedSignature"
  }
  
  def validateToken(token: String): Option[String] = {
    Try {
      val parts = token.split("\\.")
      if (parts.length != 3) return None
      
      // Decode the payload (second part)
      val payload = new String(Base64.getDecoder.decode(parts(1)))
      
      // Simple extraction - in real app would use proper JWT library
      val usernamePattern = """"sub":"([^"]+)"""".r
      usernamePattern.findFirstMatchIn(payload).map(_.group(1))
    }.toOption.flatten
  }
}