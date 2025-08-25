package models

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import java.time.LocalDateTime

class FarmSpec extends AnyFlatSpec with Matchers {

  "Farm" should "create valid farm with correct data" in {
    val producerId = 1
    val now = LocalDateTime.now()
    val farm = Farm(
      id = Some(1),
      name = "Fazenda Santa Clara",
      city = "Campinas",
      state = "SP",
      totalArea = 500.0,
      agriculturalArea = 300.0,
      vegetationArea = 200.0,
      producerId = producerId,
      createdAt = now,
      updatedAt = now
    )
    
    farm.name shouldBe "Fazenda Santa Clara"
    farm.city shouldBe "Campinas"
    farm.state shouldBe "SP"
    farm.totalArea shouldBe 500.0
    farm.agriculturalArea shouldBe 300.0
    farm.vegetationArea shouldBe 200.0
    farm.producerId shouldBe producerId
  }

  it should "validate that agricultural + vegetation areas equal total area" in {
    val now = LocalDateTime.now()
    val farm = Farm(
      id = Some(2),
      name = "Fazenda Equilibrada",
      city = "Ribeirão Preto",
      state = "SP",
      totalArea = 800.0,
      agriculturalArea = 500.0,
      vegetationArea = 300.0,
      producerId = 1,
      createdAt = now,
      updatedAt = now
    )
    
    (farm.agriculturalArea + farm.vegetationArea) shouldBe farm.totalArea
  }

  it should "support different Brazilian states" in {
    val states = List("SP", "MT", "GO", "MS", "RS", "PR", "MG", "BA")
    val now = LocalDateTime.now()
    
    states.foreach { state =>
      val farm = Farm(
        id = Some(3),
        name = s"Fazenda $state",
        city = s"Cidade $state",
        state = state,
        totalArea = 1000.0,
        agriculturalArea = 600.0,
        vegetationArea = 400.0,
        producerId = 1,
        createdAt = now,
        updatedAt = now
      )
      
      farm.state shouldBe state
    }
  }

  it should "handle fazendas with only vegetation area" in {
    val now = LocalDateTime.now()
    val farm = Farm(
      id = Some(4),
      name = "Reserva Ambiental",
      city = "Manaus",
      state = "AM",
      totalArea = 1000.0,
      agriculturalArea = 0.0,
      vegetationArea = 1000.0,
      producerId = 1,
      createdAt = now,
      updatedAt = now
    )
    
    farm.agriculturalArea shouldBe 0.0
    farm.vegetationArea shouldBe farm.totalArea
  }

  it should "handle fazendas with maximum agricultural usage" in {
    val now = LocalDateTime.now()
    val farm = Farm(
      id = Some(5),
      name = "Fazenda Produtiva",
      city = "Goiânia",
      state = "GO",
      totalArea = 800.0,
      agriculturalArea = 800.0,
      vegetationArea = 0.0,
      producerId = 1,
      createdAt = now,
      updatedAt = now
    )
    
    farm.agriculturalArea shouldBe farm.totalArea
    farm.vegetationArea shouldBe 0.0
  }

  it should "link to correct producer" in {
    val producerId = 1
    val now = LocalDateTime.now()
    
    val farm1 = Farm(
      id = Some(6),
      name = "Fazenda 1",
      city = "Cidade A",
      state = "SP",
      totalArea = 500.0,
      agriculturalArea = 300.0,
      vegetationArea = 200.0,
      producerId = producerId,
      createdAt = now,
      updatedAt = now
    )
    
    val farm2 = Farm(
      id = Some(7),
      name = "Fazenda 2",
      city = "Cidade B",
      state = "SP",
      totalArea = 700.0,
      agriculturalArea = 400.0,
      vegetationArea = 300.0,
      producerId = producerId,
      createdAt = now,
      updatedAt = now
    )
    
    farm1.producerId shouldBe producerId
    farm2.producerId shouldBe producerId
    farm1.producerId shouldBe farm2.producerId
  }
}