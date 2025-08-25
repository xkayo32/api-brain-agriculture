package models

import java.time.LocalDateTime

// Modelo do produtor rural (compatível com Python)
case class Producer(
  id: Option[Int] = None,
  document: String, // cpf ou cnpj
  name: String,
  createdAt: LocalDateTime = LocalDateTime.now(),
  updatedAt: LocalDateTime = LocalDateTime.now()
)

// Dados para criar um novo produtor
case class CreateProducerRequest(
  document: String,
  name: String
)

// Dados para atualizar produtor
case class UpdateProducerRequest(
  document: Option[String],
  name: Option[String]
)

// Response do produtor
case class ProducerResponse(
  id: Int,
  document: String,
  name: String,
  createdAt: LocalDateTime,
  updatedAt: LocalDateTime,
  farms: List[FarmResponse] = List.empty
)