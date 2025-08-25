package models

import java.util.UUID
import java.time.LocalDateTime

// Modelo do usuario
case class User(
  id: Option[UUID] = None,
  username: String,
  email: String,
  hashedPassword: String,
  isActive: Boolean = true,
  isAdmin: Boolean = false,
  createdAt: LocalDateTime = LocalDateTime.now(),
  updatedAt: LocalDateTime = LocalDateTime.now()
)

// Dados para criar usuario
case class UserRegister(
  username: String,
  email: String,
  password: String
)

// Dados para login
case class UserLogin(
  username: String,
  password: String
)

// Resposta do usuario (sem senha)
case class UserResponse(
  id: UUID,
  username: String,
  email: String,
  isActive: Boolean,
  isAdmin: Boolean,
  createdAt: LocalDateTime
)

// Token JWT
case class Token(
  accessToken: String,
  tokenType: String = "Bearer"
)