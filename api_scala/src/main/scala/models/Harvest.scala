package models

import java.time.LocalDateTime

// Modelo da safra (compatível com Python)
case class Harvest(
  id: Option[Int] = None,
  farmId: Int,
  year: Int,
  description: String, // Ex: "Safra 2024", "Safra Verão 2024"
  createdAt: LocalDateTime = LocalDateTime.now()
)

// Requisicao para criar safra
case class CreateHarvestRequest(
  farmId: Int,
  year: Int,
  description: String
)

// Response da safra
case class HarvestResponse(
  id: Int,
  farmId: Int,
  year: Int,
  description: String,
  createdAt: LocalDateTime,
  crops: List[CropResponse] = List.empty
)