CREATE DATABASE  IF NOT EXISTS `farma_norte` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `farma_norte`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: farma_norte
-- ------------------------------------------------------
-- Server version	9.5.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '1f1f6c9c-ce30-11f0-9067-1860249ddd2a:1-266,
f19f5c68-cb95-11f0-aac4-00e26908fbb7:1-51';

--
-- Table structure for table `datos_farmacia`
--

DROP TABLE IF EXISTS `datos_farmacia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_farmacia` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_farmacia` varchar(255) NOT NULL,
  `codigo_sucursal` varchar(100) NOT NULL,
  `ubicacion` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_farmacia`
--

LOCK TABLES `datos_farmacia` WRITE;
/*!40000 ALTER TABLE `datos_farmacia` DISABLE KEYS */;
INSERT INTO `datos_farmacia` VALUES (1,'Farma Norte','SUC-001','Sede Central');
/*!40000 ALTER TABLE `datos_farmacia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_movimientos`
--

DROP TABLE IF EXISTS `historial_movimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_movimientos` (
  `id_movimiento` int NOT NULL AUTO_INCREMENT,
  `id_lote` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo_movimiento` enum('Entrada','Salida') NOT NULL,
  `cantidad` int NOT NULL,
  `fecha_hora` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_movimiento`),
  KEY `id_lote` (`id_lote`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `historial_movimientos_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lote_inventario` (`id_lote`),
  CONSTRAINT `historial_movimientos_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_movimientos`
--

LOCK TABLES `historial_movimientos` WRITE;
/*!40000 ALTER TABLE `historial_movimientos` DISABLE KEYS */;
/*!40000 ALTER TABLE `historial_movimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lote_inventario`
--

DROP TABLE IF EXISTS `lote_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lote_inventario` (
  `id_lote` int NOT NULL AUTO_INCREMENT,
  `id_medicamento` int NOT NULL,
  `numero_lote` varchar(100) NOT NULL,
  `stock_actual` int DEFAULT '0',
  `fecha_vencimiento` date NOT NULL,
  PRIMARY KEY (`id_lote`),
  UNIQUE KEY `uq_medicamento_lote` (`id_medicamento`,`numero_lote`),
  CONSTRAINT `lote_inventario_ibfk_1` FOREIGN KEY (`id_medicamento`) REFERENCES `medicamentos` (`id_medicamento`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote_inventario`
--

LOCK TABLES `lote_inventario` WRITE;
/*!40000 ALTER TABLE `lote_inventario` DISABLE KEYS */;
INSERT INTO `lote_inventario` VALUES (1,1,'LOT-IBU-101',100,'2028-05-30'),(2,2,'LOT-DES-102',60,'2027-10-15'),(3,3,'LOT-ACE-103',130,'2028-03-22'),(4,4,'LOT-LOR-104',50,'2027-08-12'),(5,5,'LOT-OME-105',120,'2028-01-20'),(6,6,'LOT-DIC-106',80,'2027-12-05'),(7,7,'LOT-LOS-107',90,'2028-06-15'),(8,8,'LOT-AMO-108',40,'2027-11-30');
/*!40000 ALTER TABLE `lote_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicamentos`
--

DROP TABLE IF EXISTS `medicamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicamentos` (
  `id_medicamento` int NOT NULL AUTO_INCREMENT,
  `codigo_barra` varchar(255) DEFAULT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` text,
  `presentacion` varchar(100) DEFAULT NULL,
  `categoria` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_medicamento`),
  UNIQUE KEY `codigo_barra` (`codigo_barra`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicamentos`
--

LOCK TABLES `medicamentos` WRITE;
/*!40000 ALTER TABLE `medicamentos` DISABLE KEYS */;
INSERT INTO `medicamentos` VALUES (1,'101','Ibuprofeno 400 mg','Analgésico y antiinflamatorio no esteroideo para dolores moderados.','Caja de 20 tabletas'),(2,'102','Desloratadina 5 mg','Antihistamínico de acción prolongada que no produce somnolencia.','Caja de 10 tabletas'),(3,'103','Acetaminophen 500mg','Analgésico y antipirético para el alivio de la fiebre y malestares.','Caja de 24 tabletas'),(4,'104','Loratadina 10mg','Antihistamínico para el alivio de alergias y rinitis.','Caja de 10 tabletas'),(5,'105','Omeprazol 20mg','Protector gástrico para la acidez y reflujo.','Caja de 30 cápsulas'),(6,'106','Diclofenac Potásico 50mg','Analgésico y antiinflamatorio para dolores fuertes.','Caja de 20 tabletas'),(7,'107','Losartán Potásico 50mg','Antihipertensivo para el control de la presión alta.','Caja de 30 comprimidos'),(8,'108','Amoxicilina 500mg','Antibiótico para combatir infecciones bacterianas.','Caja de 16 cápsulas');
/*!40000 ALTER TABLE `medicamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `predicciones_demanda`
--

DROP TABLE IF EXISTS `predicciones_demanda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `predicciones_demanda` (
  `id_prediccion` int NOT NULL AUTO_INCREMENT,
  `id_medicamento` int NOT NULL,
  `fecha_prediccion` date NOT NULL,
  `cantidad_predicha` int NOT NULL,
  `factor_climatico` enum('Normal','Frente Frio','Temporada de Lluvias','Alta Temperatura') DEFAULT 'Normal',
  `probabilidad_alerta` enum('BAJA','MEDIA','ALTA') NOT NULL,
  `creado_el` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_prediccion`),
  KEY `fk_prediccion_medicamento` (`id_medicamento`),
  CONSTRAINT `fk_prediccion_medicamento` FOREIGN KEY (`id_medicamento`) REFERENCES `medicamentos` (`id_medicamento`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `predicciones_demanda`
--

LOCK TABLES `predicciones_demanda` WRITE;
/*!40000 ALTER TABLE `predicciones_demanda` DISABLE KEYS */;
INSERT INTO `predicciones_demanda` VALUES (1,1,'2026-07-14',18,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(2,1,'2026-07-15',20,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(3,1,'2026-07-16',20,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(4,1,'2026-07-17',25,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(5,1,'2026-07-18',23,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(6,1,'2026-07-19',23,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(7,1,'2026-07-20',18,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(8,2,'2026-07-14',8,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(9,2,'2026-07-15',11,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(10,2,'2026-07-16',11,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(11,2,'2026-07-17',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(12,2,'2026-07-18',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(13,2,'2026-07-19',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(14,2,'2026-07-20',8,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(15,3,'2026-07-14',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(16,3,'2026-07-15',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(17,3,'2026-07-16',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(18,3,'2026-07-17',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(19,3,'2026-07-18',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(20,3,'2026-07-19',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(21,3,'2026-07-20',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(22,4,'2026-07-14',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(23,4,'2026-07-15',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(24,4,'2026-07-16',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(25,4,'2026-07-17',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(26,4,'2026-07-18',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(27,4,'2026-07-19',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(28,4,'2026-07-20',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(29,5,'2026-07-14',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(30,5,'2026-07-15',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(31,5,'2026-07-16',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(32,5,'2026-07-17',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(33,5,'2026-07-18',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(34,5,'2026-07-19',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(35,5,'2026-07-20',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(36,6,'2026-07-14',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(37,6,'2026-07-15',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(38,6,'2026-07-16',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(39,6,'2026-07-17',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(40,6,'2026-07-18',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(41,6,'2026-07-19',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(42,6,'2026-07-20',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(43,7,'2026-07-14',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(44,7,'2026-07-15',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(45,7,'2026-07-16',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(46,7,'2026-07-17',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(47,7,'2026-07-18',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(48,7,'2026-07-19',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(49,7,'2026-07-20',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(50,8,'2026-07-14',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(51,8,'2026-07-15',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(52,8,'2026-07-16',15,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(53,8,'2026-07-17',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(54,8,'2026-07-18',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(55,8,'2026-07-19',17,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03'),(56,8,'2026-07-20',13,'Temporada de Lluvias','BAJA','2026-07-13 13:36:03');
/*!40000 ALTER TABLE `predicciones_demanda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL,
  `nombre_rol` varchar(50) NOT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Super Admin'),(2,'Administrador'),(3,'Cajero');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `pri_nom` varchar(100) NOT NULL,
  `seg_nom` varchar(100) DEFAULT NULL,
  `pri_ape` varchar(100) NOT NULL,
  `seg_ape` varchar(100) DEFAULT NULL,
  `usuario` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `id_rol` int NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Administrador','Sistema','Farma','Norte','superadmin','$2b$12$tYz2z7dhhrlPICG7AfAKuuntGMH2QfIdNJikIwj6AZVNJ4rkN4yyG',1),(2,'pepe',NULL,'Emeregildo',NULL,'pepe_gildo','$2b$12$GUNH6y7quSZ.j3cXt7qJmugCi9f0ysk2HYcNpmVKZcd/NfLY.r7vO',3),(3,'emeregildo',NULL,'gutierrez',NULL,'emegildo','$2b$12$l2JRYJv4TvTkqZcO1u4y/.ANsqCmH4.qSJvJDi1dxUft1Q2XTKyCq',3);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-14 17:57:46
