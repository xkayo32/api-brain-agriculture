package models

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import java.util.UUID

class ProducerSpec extends AnyFlatSpec with Matchers {

  "Producer" should "create valid producer" in {
    val producer = Producer(
      document = "12345678909",
      name = "João Silva"
    )
    
    producer.name shouldBe "João Silva"
    producer.document shouldBe "12345678909"
  }

  it should "create producer with minimum fields" in {
    val producer = Producer(
      document = "98765432100",
      name = "Maria Santos"
    )
    
    producer.document shouldBe "98765432100"
    producer.name shouldBe "Maria Santos"
  }

  it should "create producer with valid CPF" in {
    val producer = Producer(
      document = "11144477735", // CPF válido
      name = "Carlos Oliveira"
    )
    
    producer.document shouldBe "11144477735"
    producer.name shouldBe "Carlos Oliveira"
  }

  it should "store document without formatting" in {
    val producer = Producer(
      document = "12345678909", // CPF limpo
      name = "Ana Costa"
    )
    
    producer.document should not include "."
    producer.document should not include "-"
    producer.document.length shouldBe 11
  }

  it should "store CNPJ without formatting" in {
    val producer = Producer(
      document = "11222333000181", // CNPJ limpo
      name = "Empresa Rural Ltda"
    )
    
    producer.document should not include "."
    producer.document should not include "/"
    producer.document should not include "-"
    producer.document.length shouldBe 14
  }

  it should "have id and timestamps" in {
    val producer = Producer(
      document = "12345678909",
      name = "Fazendeiro Teste"
    )
    
    producer.id shouldBe None // Novo producer sem ID
    producer.createdAt shouldBe a[java.time.LocalDateTime]
    producer.updatedAt shouldBe a[java.time.LocalDateTime]
  }

}