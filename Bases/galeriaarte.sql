-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: galeriaarte
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `autor`
--

DROP TABLE IF EXISTS `autor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `autor` (
  `PessoaID` int NOT NULL,
  `MatriculaAutor` varchar(15) NOT NULL,
  `NomeUsuario` varchar(30) NOT NULL,
  `Senha` varchar(255) NOT NULL,
  PRIMARY KEY (`PessoaID`),
  UNIQUE KEY `MatriculaAutor` (`MatriculaAutor`),
  CONSTRAINT `autor_ibfk_1` FOREIGN KEY (`PessoaID`) REFERENCES `pessoa` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autor`
--

LOCK TABLES `autor` WRITE;
/*!40000 ALTER TABLE `autor` DISABLE KEYS */;
/*!40000 ALTER TABLE `autor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `PessoaID` int NOT NULL,
  `MatriculaCliente` varchar(15) NOT NULL,
  `QuantidadeObrasCompradas` int DEFAULT '0',
  `NomeUsuario` varchar(30) NOT NULL,
  `Senha` varchar(255) NOT NULL,
  `Recomendações` text,
  PRIMARY KEY (`PessoaID`),
  UNIQUE KEY `MatriculaCliente` (`MatriculaCliente`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`PessoaID`) REFERENCES `pessoa` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `endereco`
--

DROP TABLE IF EXISTS `endereco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `endereco` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `PessoaID` int NOT NULL,
  `Rua` varchar(200) NOT NULL,
  `Numero` varchar(10) NOT NULL,
  `Bairro` varchar(100) NOT NULL,
  `Cidade` varchar(100) NOT NULL,
  `Estado` varchar(2) NOT NULL,
  `CEP` varchar(8) NOT NULL,
  `Pais` varchar(4) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `PessoaID` (`PessoaID`),
  CONSTRAINT `endereco_ibfk_1` FOREIGN KEY (`PessoaID`) REFERENCES `pessoa` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endereco`
--

LOCK TABLES `endereco` WRITE;
/*!40000 ALTER TABLE `endereco` DISABLE KEYS */;
/*!40000 ALTER TABLE `endereco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionario`
--

DROP TABLE IF EXISTS `funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionario` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `PessoaID` int NOT NULL,
  `NomeUsuario` varchar(30) NOT NULL,
  `Senha` varchar(255) NOT NULL,
  `Cargo` varchar(30) NOT NULL,
  `DataContratacao` date NOT NULL,
  `Salario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `NomeUsuario` (`NomeUsuario`),
  KEY `PessoaID` (`PessoaID`),
  CONSTRAINT `funcionario_ibfk_1` FOREIGN KEY (`PessoaID`) REFERENCES `pessoa` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionario`
--

LOCK TABLES `funcionario` WRITE;
/*!40000 ALTER TABLE `funcionario` DISABLE KEYS */;
/*!40000 ALTER TABLE `funcionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `galeria`
--

DROP TABLE IF EXISTS `galeria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `galeria` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ObraID` int NOT NULL,
  `Valor` decimal(11,2) NOT NULL,
  `Status` tinyint NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ObraID` (`ObraID`),
  CONSTRAINT `galeria_ibfk_1` FOREIGN KEY (`ObraID`) REFERENCES `obradearte` (`ID`),
  CONSTRAINT `galeria_chk_1` CHECK ((`Status` in (0,1,2)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `galeria`
--

LOCK TABLES `galeria` WRITE;
/*!40000 ALTER TABLE `galeria` DISABLE KEYS */;
/*!40000 ALTER TABLE `galeria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obradearte`
--

DROP TABLE IF EXISTS `obradearte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obradearte` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Imagem` longblob,
  `TipoArquivo` varchar(10) NOT NULL,
  `Titulo` varchar(200) NOT NULL,
  `Descricao` text,
  `DataPublicacao` date NOT NULL,
  `EstiloArte` varchar(60) NOT NULL,
  `AutorID` int NOT NULL,
  `PaisGaleria` varchar(4) NOT NULL,
  `Altura` float NOT NULL,
  `Largura` float NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `AutorID` (`AutorID`),
  CONSTRAINT `obradearte_ibfk_1` FOREIGN KEY (`AutorID`) REFERENCES `autor` (`PessoaID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obradearte`
--

LOCK TABLES `obradearte` WRITE;
/*!40000 ALTER TABLE `obradearte` DISABLE KEYS */;
/*!40000 ALTER TABLE `obradearte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagamento`
--

DROP TABLE IF EXISTS `pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagamento` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VendaID` int NOT NULL,
  `ValorTotalPago` decimal(10,2) NOT NULL,
  `MetodoPagamento` varchar(20) NOT NULL,
  `Situacao` tinyint NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `VendaID` (`VendaID`),
  CONSTRAINT `pagamento_ibfk_1` FOREIGN KEY (`VendaID`) REFERENCES `venda` (`ID`),
  CONSTRAINT `pagamento_chk_1` CHECK ((`Situacao` in (1,2)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagamento`
--

LOCK TABLES `pagamento` WRITE;
/*!40000 ALTER TABLE `pagamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `VendaID` int NOT NULL,
  `ObraID` int NOT NULL,
  `Valor` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `VendaID` (`VendaID`),
  KEY `ObraID` (`ObraID`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`VendaID`) REFERENCES `venda` (`ID`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`ObraID`) REFERENCES `obradearte` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pessoa`
--

DROP TABLE IF EXISTS `pessoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pessoa` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(100) NOT NULL,
  `Sobrenome` varchar(100) NOT NULL,
  `CPF` varchar(11) NOT NULL,
  `DataNascimento` date NOT NULL,
  `Email` varchar(100) NOT NULL,
  `NomeUsuario` varchar(30) NOT NULL,
  `Senha` varchar(255) NOT NULL,
  `Telefone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `CPF` (`CPF`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `NomeUsuario` (`NomeUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pessoa`
--

LOCK TABLES `pessoa` WRITE;
/*!40000 ALTER TABLE `pessoa` DISABLE KEYS */;
/*!40000 ALTER TABLE `pessoa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venda`
--

DROP TABLE IF EXISTS `venda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venda` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ClienteID` int NOT NULL,
  `FuncionarioID` int NOT NULL,
  `PedidoID` varchar(20) NOT NULL,
  `ValorTotal` decimal(10,2) NOT NULL,
  `DataVenda` date NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `PedidoID` (`PedidoID`),
  KEY `ClienteID` (`ClienteID`),
  KEY `FuncionarioID` (`FuncionarioID`),
  CONSTRAINT `venda_ibfk_1` FOREIGN KEY (`ClienteID`) REFERENCES `cliente` (`PessoaID`),
  CONSTRAINT `venda_ibfk_2` FOREIGN KEY (`FuncionarioID`) REFERENCES `funcionario` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venda`
--

LOCK TABLES `venda` WRITE;
/*!40000 ALTER TABLE `venda` DISABLE KEYS */;
/*!40000 ALTER TABLE `venda` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-22  1:44:46
