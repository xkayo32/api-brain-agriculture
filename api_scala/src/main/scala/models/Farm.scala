package models

import java.time.LocalDateTime

// Modelo da fazenda (compatível com Python)
case class Farm(
  id: Option[Int] = None,
  producerId: Int,
  name: String,
  city: String,
  state: String,
  totalArea: Double, // area em hectares
  agriculturalArea: Double,
  vegetationArea: Double,
  createdAt: LocalDateTime = LocalDateTime.now(),
  updatedAt: LocalDateTime = LocalDateTime.now()
)

// Requisicao para criar fazenda
case class CreateFarmRequest(
  producerId: Int,
  name: String,
  city: String,
  state: String,
  totalArea: Double,
  agriculturalArea: Double,
  vegetationArea: Double
)

// Requisicao para atualizar fazenda
case class UpdateFarmRequest(
  name: Option[String],
  city: Option[String],
  state: Option[String],
  totalArea: Option[Double],
  agriculturalArea: Option[Double],
  vegetationArea: Option[Double]
)

// Response da fazenda
case class FarmResponse(
  id: Int,
  producerId: Int,
  name: String,
  city: String,
  state: String,
  totalArea: Double,
  agriculturalArea: Double,
  vegetationArea: Double,
  createdAt: LocalDateTime,
  updatedAt: LocalDateTime,
  harvests: List[HarvestResponse] = List.empty
)