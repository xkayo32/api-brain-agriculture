package utils

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class DocumentValidatorSpec extends AnyFlatSpec with Matchers {

  "DocumentValidator" should "validate valid CPF numbers" in {
    DocumentValidator.validateCPF("11144477735") shouldBe true
    DocumentValidator.validateCPF("12345678909") shouldBe true
    DocumentValidator.validateCPF("98765432100") shouldBe true
  }

  it should "validate CPF with formatting" in {
    DocumentValidator.validateCPF("111.444.777-35") shouldBe true
    DocumentValidator.validateCPF("123.456.789-09") shouldBe true
    DocumentValidator.validateCPF("987.654.321-00") shouldBe true
  }

  it should "reject invalid CPF numbers" in {
    DocumentValidator.validateCPF("11144477736") shouldBe false // digito errado
    DocumentValidator.validateCPF("11144477725") shouldBe false // digito errado
    DocumentValidator.validateCPF("12345678901") shouldBe false // digitos errados
  }

  it should "reject CPF with all same digits" in {
    DocumentValidator.validateCPF("11111111111") shouldBe false
    DocumentValidator.validateCPF("22222222222") shouldBe false
    DocumentValidator.validateCPF("00000000000") shouldBe false
  }

  it should "reject CPF with invalid length" in {
    DocumentValidator.validateCPF("1234567890") shouldBe false   // 10 digitos
    DocumentValidator.validateCPF("123456789012") shouldBe false // 12 digitos
    DocumentValidator.validateCPF("") shouldBe false             // vazio
    DocumentValidator.validateCPF("abc") shouldBe false          // muito pequeno
  }

  it should "reject CPF with non-numeric characters" in {
    DocumentValidator.validateCPF("1234567890a") shouldBe false
    DocumentValidator.validateCPF("abcdefghijk") shouldBe false
  }

  "DocumentValidator" should "validate valid CNPJ numbers" in {
    DocumentValidator.validateCNPJ("11222333000181") shouldBe true
    DocumentValidator.validateCNPJ("11444777000161") shouldBe true
  }

  it should "validate CNPJ with formatting" in {
    DocumentValidator.validateCNPJ("11.222.333/0001-81") shouldBe true
    DocumentValidator.validateCNPJ("11.444.777/0001-61") shouldBe true
  }

  it should "reject invalid CNPJ numbers" in {
    DocumentValidator.validateCNPJ("11222333000192") shouldBe false // digito errado
    DocumentValidator.validateCNPJ("11222333000171") shouldBe false // digito errado
  }

  it should "reject CNPJ with all same digits" in {
    DocumentValidator.validateCNPJ("11111111111111") shouldBe false
    DocumentValidator.validateCNPJ("00000000000000") shouldBe false
  }

  it should "reject CNPJ with invalid length" in {
    DocumentValidator.validateCNPJ("1122233300018") shouldBe false   // 13 digitos
    DocumentValidator.validateCNPJ("112223330001812") shouldBe false // 15 digitos
    DocumentValidator.validateCNPJ("") shouldBe false                // vazio
  }

  "DocumentValidator" should "validate documents generically" in {
    // CPF valido
    DocumentValidator.validateDocument("11144477735") shouldBe true
    DocumentValidator.validateDocument("111.444.777-35") shouldBe true
    
    // CNPJ valido
    DocumentValidator.validateDocument("11222333000181") shouldBe true
    DocumentValidator.validateDocument("11.222.333/0001-81") shouldBe true
    
    // Documentos invalidos
    DocumentValidator.validateDocument("11144477736") shouldBe false
    DocumentValidator.validateDocument("11222333000192") shouldBe false
    DocumentValidator.validateDocument("123456789") shouldBe false     // tamanho invalido
    DocumentValidator.validateDocument("123456789012345") shouldBe false // muito grande
  }

  "DocumentValidator" should "format CPF correctly" in {
    DocumentValidator.formatDocument("11144477735") shouldBe "111.444.777-35"
    DocumentValidator.formatDocument("12345678909") shouldBe "123.456.789-09"
  }

  it should "format CNPJ correctly" in {
    DocumentValidator.formatDocument("11222333000181") shouldBe "11.222.333/0001-81"
    DocumentValidator.formatDocument("11444777000161") shouldBe "11.444.777/0001-61"
  }

  it should "return document as-is if already formatted" in {
    DocumentValidator.formatDocument("111.444.777-35") shouldBe "111.444.777-35"
    DocumentValidator.formatDocument("11.222.333/0001-81") shouldBe "11.222.333/0001-81"
  }

  it should "return invalid documents as-is when formatting" in {
    DocumentValidator.formatDocument("123") shouldBe "123"
    DocumentValidator.formatDocument("invalid") shouldBe "invalid"
  }
}