package models

import java.time.LocalDateTime

// Tipos de cultura (compatível com Python)
object CropType extends Enumeration {
  type CropType = Value
  val SOJA = Value("SOJA")
  val MILHO = Value("MILHO")
  val ALGODAO = Value("ALGODAO")
  val CAFE = Value("CAFE")
  val CANA_DE_ACUCAR = Value("CANA_DE_ACUCAR")
}

// Modelo da cultura plantada (compatível com Python)
case class Crop(
  id: Option[Int] = None,
  harvestId: Int,
  cropType: CropType.CropType,
  plantedArea: Double, // area em hectares
  createdAt: LocalDateTime = LocalDateTime.now()
)

// Requisicao para criar cultura
case class CreateCropRequest(
  harvestId: Int,
  cropType: String,
  plantedArea: Double
)

// Response da cultura
case class CropResponse(
  id: Int,
  harvestId: Int,
  cropType: String,
  plantedArea: Double,
  createdAt: LocalDateTime
)