-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: farma_norte
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Dumping data for table `lote_inventario`
--

LOCK TABLES `lote_inventario` WRITE;
/*!40000 ALTER TABLE `lote_inventario` DISABLE KEYS */;
INSERT INTO `lote_inventario` VALUES (1,1,'LOT-IBU-101',100,'2028-05-30'),(2,2,'LOT-DES-102',60,'2027-10-15'),(3,3,'LOT-ACE-103',130,'2028-03-22'),(4,4,'LOT-LOR-104',50,'2027-08-12'),(5,5,'LOT-OME-105',120,'2028-01-20'),(6,6,'LOT-DIC-106',80,'2027-12-05'),(7,7,'LOT-LOS-107',90,'2028-06-15'),(8,8,'LOT-AMO-108',40,'2027-11-30');
/*!40000 ALTER TABLE `lote_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `medicamentos`
--

LOCK TABLES `medicamentos` WRITE;
/*!40000 ALTER TABLE `medicamentos` DISABLE KEYS */;
INSERT INTO `medicamentos` VALUES (1,'101','Ibuprofeno 400 mg','Analgésico y antiinflamatorio no esteroideo para dolores moderados.','Caja de 20 tabletas'),(2,'102','Desloratadina 5 mg','Antihistamínico de acción prolongada que no produce somnolencia.','Caja de 10 tabletas'),(3,'103','Acetaminophen 500mg','Analgésico y antipirético para el alivio de la fiebre y malestares.','Caja de 24 tabletas'),(4,'104','Loratadina 10mg','Antihistamínico para el alivio de alergias y rinitis.','Caja de 10 tabletas'),(5,'105','Omeprazol 20mg','Protector gástrico para la acidez y reflujo.','Caja de 30 cápsulas'),(6,'106','Diclofenac Potásico 50mg','Analgésico y antiinflamatorio para dolores fuertes.','Caja de 20 tabletas'),(7,'107','Losartán Potásico 50mg','Antihipertensivo para el control de la presión alta.','Caja de 30 comprimidos'),(8,'108','Amoxicilina 500mg','Antibiótico para combatir infecciones bacterianas.','Caja de 16 cápsulas');
/*!40000 ALTER TABLE `medicamentos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-04 23:29:53
