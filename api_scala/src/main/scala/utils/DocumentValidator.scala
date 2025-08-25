package utils

object DocumentValidator {
  
  def isValid(document: String): Boolean = {
    val cleanDoc = document.replaceAll("[^0-9]", "")
    cleanDoc.length == 11 || cleanDoc.length == 14 // CPF ou CNPJ
  }
  
  def validateCPF(cpf: String): Boolean = {
    val cleanCpf = cpf.replaceAll("[^0-9]", "")
    
    if (cleanCpf.length != 11) return false
    if (cleanCpf.matches("(\\d)\\1{10}")) return false // todos dígitos iguais
    
    val digits = cleanCpf.map(_.asDigit)
    
    // Primeiro dígito verificador
    val sum1 = (0 until 9).map(i => digits(i) * (10 - i)).sum
    val checkDigit1 = 11 - (sum1 % 11)
    val digit1 = if (checkDigit1 >= 10) 0 else checkDigit1
    
    if (digits(9) != digit1) return false
    
    // Segundo dígito verificador
    val sum2 = (0 until 10).map(i => digits(i) * (11 - i)).sum
    val checkDigit2 = 11 - (sum2 % 11)
    val digit2 = if (checkDigit2 >= 10) 0 else checkDigit2
    
    digits(10) == digit2
  }
  
  def validateCNPJ(cnpj: String): Boolean = {
    val cleanCnpj = cnpj.replaceAll("[^0-9]", "")
    
    if (cleanCnpj.length != 14) return false
    if (cleanCnpj.matches("(\\d)\\1{13}")) return false // todos dígitos iguais
    
    val digits = cleanCnpj.map(_.asDigit)
    val weights1 = Array(5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    val weights2 = Array(6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    
    // Primeiro dígito verificador
    val sum1 = (0 until 12).map(i => digits(i) * weights1(i)).sum
    val checkDigit1 = 11 - (sum1 % 11)
    val digit1 = if (checkDigit1 >= 10) 0 else checkDigit1
    
    if (digits(12) != digit1) return false
    
    // Segundo dígito verificador
    val sum2 = (0 until 13).map(i => digits(i) * weights2(i)).sum
    val checkDigit2 = 11 - (sum2 % 11)
    val digit2 = if (checkDigit2 >= 10) 0 else checkDigit2
    
    digits(13) == digit2
  }
  
  def validateDocument(document: String): Boolean = {
    val cleanDoc = document.replaceAll("[^0-9]", "")
    cleanDoc.length match {
      case 11 => validateCPF(cleanDoc)
      case 14 => validateCNPJ(cleanDoc)
      case _ => false
    }
  }
  
  def formatDocument(document: String): String = {
    val cleanDoc = document.replaceAll("[^0-9]", "")
    cleanDoc.length match {
      case 11 => 
        if (cleanDoc.matches("\\d{11}")) {
          s"${cleanDoc.substring(0,3)}.${cleanDoc.substring(3,6)}.${cleanDoc.substring(6,9)}-${cleanDoc.substring(9)}"
        } else document
      case 14 => 
        if (cleanDoc.matches("\\d{14}")) {
          s"${cleanDoc.substring(0,2)}.${cleanDoc.substring(2,5)}.${cleanDoc.substring(5,8)}/${cleanDoc.substring(8,12)}-${cleanDoc.substring(12)}"
        } else document
      case _ => document
    }
  }
}