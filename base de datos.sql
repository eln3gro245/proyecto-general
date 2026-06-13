CREATE DATABASE  IF NOT EXISTS `farmanorte_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `farmanorte_db`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: farmanorte_db
-- ------------------------------------------------------
-- Server version	9.7.0

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

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '8b58ef61-6053-11f1-b588-9840bb08bdf0:1-21';

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `Id_categoria` int NOT NULL AUTO_INCREMENT,
  `Nombre_categoria` varchar(100) NOT NULL,
  `Descripcion` text,
  PRIMARY KEY (`Id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Analgésicos','Medicamentos para aliviar el dolor físico y muscular'),(2,'Antibióticos','Fármacos para combatir infecciones bacterianas'),(3,'Antialérgicos','Tratamientos para alergias y respuestas histamínicas'),(4,'Vitaminas','Suplementos para el fortalecimiento del sistema inmunológico'),(5,'Cardiovasculares','Medicamentos para la presión arterial y control cardíaco'),(6,'Analgésicos','Medicamentos para aliviar el dolor físico y muscular'),(7,'Antibióticos','Fármacos para combatir infecciones bacterianas'),(8,'Antialérgicos','Tratamientos para alergias y respuestas histamínicas'),(9,'Vitaminas','Suplementos para el fortalecimiento del sistema inmunológico'),(10,'Cardiovasculares','Medicamentos para la presión arterial y control cardíaco'),(11,'Analgésicos','Medicamentos para aliviar el dolor físico y muscular'),(12,'Antibióticos','Fármacos para combatir infecciones bacterianas'),(13,'Antialérgicos','Tratamientos para alergias y respuestas histamínicas'),(14,'Vitaminas','Suplementos para el fortalecimiento del sistema inmunológico'),(15,'Cardiovasculares','Medicamentos para la presión arterial y control cardíaco'),(16,'Analgésicos','Medicamentos para aliviar el dolor físico y muscular'),(17,'Antibióticos','Fármacos para combatir infecciones bacterianas'),(18,'Antialérgicos','Tratamientos para alergias y respuestas histamínicas'),(19,'Vitaminas','Suplementos para el fortalecimiento del sistema inmunológico'),(20,'Cardiovasculares','Medicamentos para la presión arterial y control cardíaco');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_ventas`
--

DROP TABLE IF EXISTS `detalles_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_ventas` (
  `Id_detalle` int NOT NULL AUTO_INCREMENT,
  `Id_ventas` int DEFAULT NULL,
  `Id_producto` int DEFAULT NULL,
  `Cantidad` int NOT NULL,
  `Precio_unitario` decimal(7,2) NOT NULL,
  `Subtotal` decimal(7,2) NOT NULL,
  PRIMARY KEY (`Id_detalle`),
  KEY `Id_ventas` (`Id_ventas`),
  KEY `Id_producto` (`Id_producto`),
  CONSTRAINT `detalles_ventas_ibfk_1` FOREIGN KEY (`Id_ventas`) REFERENCES `ventas` (`Id_ventas`),
  CONSTRAINT `detalles_ventas_ibfk_2` FOREIGN KEY (`Id_producto`) REFERENCES `productos` (`Id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_ventas`
--

LOCK TABLES `detalles_ventas` WRITE;
/*!40000 ALTER TABLE `detalles_ventas` DISABLE KEYS */;
INSERT INTO `detalles_ventas` VALUES (1,1,1,2,1.50,3.00),(2,1,2,1,2.00,2.00),(3,2,3,2,4.50,9.00),(4,2,1,1,1.50,1.50),(5,3,5,1,3.00,3.00),(6,4,4,2,1.20,2.40),(7,4,1,1,1.50,1.50);
/*!40000 ALTER TABLE `detalles_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ia`
--

DROP TABLE IF EXISTS `ia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ia` (
  `Id_IA` int NOT NULL AUTO_INCREMENT,
  `Id_producto` int DEFAULT NULL,
  `Tipo_evento` varchar(20) NOT NULL,
  `Valor1` varchar(20) DEFAULT NULL,
  `valor2` varchar(20) DEFAULT NULL,
  `Confianza` decimal(5,2) DEFAULT NULL,
  `descripcion` text,
  `Fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id_IA`),
  KEY `Id_producto` (`Id_producto`),
  CONSTRAINT `ia_ibfk_1` FOREIGN KEY (`Id_producto`) REFERENCES `productos` (`Id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ia`
--

LOCK TABLES `ia` WRITE;
/*!40000 ALTER TABLE `ia` DISABLE KEYS */;
INSERT INTO `ia` VALUES (1,2,'Prediccion_Stock','Agotamiento_7_dias','Alta_Demanda',94.50,'El Ibuprofeno muestra un incremento de ventas por temporada de lluvias.','2026-06-08 03:58:37'),(2,4,'Alerta_IA','Pedido_Urgente','Stock_Critico',98.20,'Loratadina por debajo del mínimo de seguridad. Se sugiere orden de compra automática a Laboratorios Elmor.','2026-06-08 03:58:37');
/*!40000 ALTER TABLE `ia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos`
--

DROP TABLE IF EXISTS `movimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos` (
  `Id_movimiento` int NOT NULL AUTO_INCREMENT,
  `Id_producto` int DEFAULT NULL,
  `Tipo_movimiento` varchar(25) NOT NULL,
  `Cantidad` int NOT NULL,
  `Fecha_movimientos` datetime DEFAULT CURRENT_TIMESTAMP,
  `Fecha_vencimiento` date DEFAULT NULL,
  `referencia` varchar(20) DEFAULT NULL,
  `Descripcion` text,
  PRIMARY KEY (`Id_movimiento`),
  KEY `Id_producto` (`Id_producto`),
  CONSTRAINT `movimientos_ibfk_1` FOREIGN KEY (`Id_producto`) REFERENCES `productos` (`Id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos`
--

LOCK TABLES `movimientos` WRITE;
/*!40000 ALTER TABLE `movimientos` DISABLE KEYS */;
/*!40000 ALTER TABLE `movimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `Id_producto` int NOT NULL AUTO_INCREMENT,
  `Codigo_barra` varchar(20) NOT NULL,
  `Nombre_producto` varchar(150) NOT NULL,
  `Descripcion` text,
  `Precio_compra` decimal(7,2) NOT NULL,
  `Precio_venta` decimal(7,2) NOT NULL,
  `Stock_minimo` int DEFAULT '0',
  `Stock_actual` int DEFAULT '0',
  `Id_categoria` int DEFAULT NULL,
  `Id_proveedor` int DEFAULT NULL,
  `Imagen` text,
  PRIMARY KEY (`Id_producto`),
  UNIQUE KEY `Codigo_barra` (`Codigo_barra`),
  KEY `Id_categoria` (`Id_categoria`),
  KEY `Id_proveedor` (`Id_proveedor`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`Id_categoria`) REFERENCES `categorias` (`Id_categoria`),
  CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`Id_proveedor`) REFERENCES `proveedores` (`Id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'7591234560011','Acetaminofén 500mg (Elmor)','Caja de 20 tabletas para el alivio del dolor',0.90,1.50,20,120,1,1,'url_imagen_acetaminofen.png'),(2,'7593216540022','Ibuprofeno 400mg (Calox)','Analgésico y antiinflamatorio potente',1.10,2.00,30,15,1,3,'url_imagen_ibuprofeno.png'),(3,'7597891230033','Amoxicilina 500mg','Antibiótico de amplio espectro bacteriano',2.80,4.50,15,80,2,2,'url_imagen_amoxicilina.png'),(4,'7594561230044','Loratadina 10mg (Elmor)','Antihistamínico para el control de alergias',0.70,1.20,10,8,3,1,'url_imagen_loratadina.png'),(5,'4002051300555','Vitamina C 1g (Bayer)','Tabletas efervescentes sabor a naranja',1.80,3.00,15,50,4,4,'url_imagen_vitaminac.png'),(6,'7599873210066','Losartán Potásico 50mg','Tratamiento regulador de la presión arterial',1.50,2.80,10,10,5,3,'url_imagen_losartan.png');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `Id_proveedor` int NOT NULL AUTO_INCREMENT,
  `Nombre_empresa` varchar(25) NOT NULL,
  `Rif` varchar(25) NOT NULL,
  `Telefono` varchar(20) DEFAULT NULL,
  `Direccion` text,
  `Correo` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Id_proveedor`),
  UNIQUE KEY `Rif` (`Rif`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Laboratorios Elmor','J-12345678-0','0414-1234567','Zona Industrial, Caracas','contacto@elmor.com'),(2,'Droguería Nena','J-87654321-1','0424-7654321','Av. Intercomunal, Barquisimeto','ventas@droguerianena.com'),(3,'Calox International','J-45678912-3','0412-9876543','Av. Principal, Valencia','pedidos@calox.com'),(4,'Bayer de Venezuela','J-98765432-4','0212-5551122','Las Mercedes, Caracas','atencion@bayer.ve');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `Id_usuario` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(20) NOT NULL,
  `Apellido` varchar(20) NOT NULL,
  `Correo` varchar(30) NOT NULL,
  `Password_hash` varchar(20) NOT NULL,
  `Rol` varchar(15) NOT NULL,
  `Telefono` varchar(20) DEFAULT NULL,
  `Fecha_Registro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id_usuario`),
  UNIQUE KEY `Correo` (`Correo`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Juan','Ollarves','carlos@farmaNor.com','admin123','Administrador',NULL,'2026-06-08 03:37:11'),(2,'David','Mavares','davi@farmaNor.com','davi456','Cajero',NULL,'2026-06-08 03:37:11'),(3,'Jose','Hernandez','joss@farmaNor.com','joss789','Cajero',NULL,'2026-06-08 03:37:11'),(4,'Gianluca','Strippoli','gian@farmasur.com','gianb101','Cajero',NULL,'2026-06-08 03:37:11');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `Id_ventas` int NOT NULL AUTO_INCREMENT,
  `Id_usuario` int DEFAULT NULL,
  `Fecha_venta` datetime DEFAULT CURRENT_TIMESTAMP,
  `Total_decimal` decimal(7,2) NOT NULL,
  PRIMARY KEY (`Id_ventas`),
  KEY `Id_usuario` (`Id_usuario`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`Id_usuario`) REFERENCES `usuarios` (`Id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,2,'2026-06-07 09:15:00',5.00),(2,3,'2026-06-07 14:30:00',10.50),(3,4,'2026-06-08 08:00:00',3.00),(4,2,'2026-06-08 10:22:15',4.50);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
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

-- Dump completed on 2026-06-08  4:22:51
