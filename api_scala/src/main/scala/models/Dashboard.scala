package models

// Modelos para o dashboard
case class DashboardSummary(
  totalFarms: Int,
  totalArea: Double
)

case class StateDistribution(
  state: String,
  count: Int,
  percentage: Double
)

case class CropDistribution(
  cropType: String,
  totalArea: Double,
  percentage: Double
)

case class LandUseDistribution(
  agriculturalArea: Double,
  vegetationArea: Double,
  agriculturalPercentage: Double,
  vegetationPercentage: Double
)