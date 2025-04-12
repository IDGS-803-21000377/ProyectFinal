-- MySQL dump 10.13  Distrib 9.0.1, for Win64 (x86_64)
--
-- Host: localhost    Database: galletasdb
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `idDetalle` int NOT NULL AUTO_INCREMENT,
  `idPedido` int NOT NULL,
  `idProductoTerminado` int NOT NULL,
  `presentacion` varchar(150) NOT NULL,
  `cantidad` int NOT NULL,
  `subtotal` float NOT NULL,
  PRIMARY KEY (`idDetalle`),
  KEY `idPedido` (`idPedido`),
  KEY `idProductoTerminado` (`idProductoTerminado`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`idPedido`),
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`idProductoTerminado`) REFERENCES `productos_terminados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` VALUES (1,1,1,'individual',10,80),(2,2,6,'caja',2,180);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleventa`
--

DROP TABLE IF EXISTS `detalleventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleventa` (
  `idDetalleVenta` int NOT NULL AUTO_INCREMENT,
  `idVenta` int NOT NULL,
  `idProductoTerminado` int NOT NULL,
  `cantidad` int NOT NULL,
  `presentacion` varchar(50) NOT NULL,
  `subtotal` float NOT NULL,
  PRIMARY KEY (`idDetalleVenta`),
  KEY `idVenta` (`idVenta`),
  KEY `idProductoTerminado` (`idProductoTerminado`),
  CONSTRAINT `detalleventa_ibfk_1` FOREIGN KEY (`idVenta`) REFERENCES `venta` (`idVenta`),
  CONSTRAINT `detalleventa_ibfk_2` FOREIGN KEY (`idProductoTerminado`) REFERENCES `productos_terminados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleventa`
--

LOCK TABLES `detalleventa` WRITE;
/*!40000 ALTER TABLE `detalleventa` DISABLE KEYS */;
INSERT INTO `detalleventa` VALUES (1,1,1,3,'caja',270),(2,4,7,10,'individual',80),(3,5,1,10,'individual',80),(4,6,8,20,'individual',160),(5,7,6,2,'caja',180),(6,8,10,3,'caja',270);
/*!40000 ALTER TABLE `detalleventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `error_logs`
--

DROP TABLE IF EXISTS `error_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `error_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `path` varchar(255) DEFAULT NULL,
  `message` text,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `error_logs`
--

LOCK TABLES `error_logs` WRITE;
/*!40000 ALTER TABLE `error_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `error_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materias_primas`
--

DROP TABLE IF EXISTS `materias_primas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materias_primas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `cantidad_disponible` float NOT NULL,
  `unidad` varchar(20) DEFAULT NULL,
  `precio_por_unidad` float NOT NULL,
  `proveedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedor_id` (`proveedor_id`),
  CONSTRAINT `materias_primas_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias_primas`
--

LOCK TABLES `materias_primas` WRITE;
/*!40000 ALTER TABLE `materias_primas` DISABLE KEYS */;
INSERT INTO `materias_primas` VALUES (3,'Chocolate',10,'kg',1500,3),(4,'Mantequilla',7.6,'kg',1900,3),(5,'Azucar blanca',8.5,'kg',400,3),(6,'Azucar Morena',8.5,'kg',450,3),(7,'Huevo',80,'Pieza',400,3),(8,'Escencia de vainilla',6.25,'Lt',1900,3),(9,'Harina de trigo',10,'kg',900,3),(10,'Bicarbonato',4.7,'kg',500,3),(11,'Sal',9.976,'kg',500,3),(12,'Fresa',8.5,'kg',300,3),(13,'Nuez',10,'kg',600,3),(14,'Bombon',8.5,'kg',600,3),(15,'Jugo de Limon',9.85,'Lt',500,3),(16,'Limon',50,'Pieza',450,3);
/*!40000 ALTER TABLE `materias_primas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `idPedido` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `fecha_recoleccion` date NOT NULL,
  `fecha` date NOT NULL,
  `estatus` varchar(10) NOT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,4,'2025-04-24','2025-04-11','vendido'),(2,4,'2025-04-24','2025-04-12','vendido');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_terminados`
--

DROP TABLE IF EXISTS `productos_terminados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_terminados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `cantidad` float NOT NULL,
  `fecha_produccion` datetime DEFAULT NULL,
  `receta_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  CONSTRAINT `productos_terminados_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_terminados`
--

LOCK TABLES `productos_terminados` WRITE;
/*!40000 ALTER TABLE `productos_terminados` DISABLE KEYS */;
INSERT INTO `productos_terminados` VALUES (1,'Galletas de chocolate','Receta para 300 galletas',830,'2025-04-11 17:29:07',1),(3,'Galletas de fresa','Receta para 300 galletas',300,'2025-04-11 18:30:50',3),(6,'Galletas de nuez','Receta para 300 galletas',260,'2025-04-11 18:47:14',6),(7,'Galletas de bombon','Receta para 300 galletas',290,'2025-04-11 18:49:39',7),(8,'Galletas de limon','Receta para 300 galletas',280,'2025-04-11 18:59:35',8),(9,'Galletas rellenas de Nutella','Receta para 300 galletas',300,'2025-04-11 19:05:52',9),(10,'Galletas de vainilla','Receta de 300 galletas',540,'2025-04-12 00:23:57',10);
/*!40000 ALTER TABLE `productos_terminados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Proveedor Jorge Rangel','Universidad Tecnologica #D','4776944082',NULL),(3,'Proveedor Gerardo','Universidad Tecnologica #B','4771153717',NULL);
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (1,'Galletas de chocolate','Receta para 300 galletas','galletachoco.jpg'),(3,'Galletas de fresa','Receta para 300 galletas','fresa.jpg'),(6,'Galletas de nuez','Receta para 300 galletas','nuez.jpg'),(7,'Galletas de bombon','Receta para 300 galletas','bombon.jpg'),(8,'Galletas de limon','Receta para 300 galletas','limon.jpg'),(9,'Galletas rellenas de Nutella','Receta para 300 galletas','nutella.jpg'),(10,'Galletas de vainilla','Receta de 300 galletas','vainilla.jpg');
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas_ingredientes`
--

DROP TABLE IF EXISTS `recetas_ingredientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas_ingredientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int NOT NULL,
  `materia_prima_id` int NOT NULL,
  `cantidad` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  CONSTRAINT `recetas_ingredientes_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`),
  CONSTRAINT `recetas_ingredientes_ibfk_2` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas_ingredientes`
--

LOCK TABLES `recetas_ingredientes` WRITE;
/*!40000 ALTER TABLE `recetas_ingredientes` DISABLE KEYS */;
INSERT INTO `recetas_ingredientes` VALUES (1,1,3,1.5),(2,1,4,1.2),(3,1,5,0.75),(4,1,6,0.75),(5,1,7,10),(6,1,8,0.075),(7,1,9,1.5),(8,1,10,0.025),(9,1,11,0.012),(11,3,4,1.2),(12,3,5,0.75),(13,3,6,0.75),(14,3,7,10),(15,3,8,0.075),(16,3,9,1.5),(17,3,10,0.025),(18,3,11,0.012),(19,3,12,1.5),(37,6,4,1.2),(38,6,5,0.75),(39,6,6,0.75),(40,6,7,10),(41,6,8,0.075),(42,6,9,1.5),(43,6,10,0.025),(44,6,11,0.012),(45,6,13,1.5),(46,7,4,1.2),(47,7,5,0.75),(48,7,6,0.75),(49,7,7,10),(50,7,8,0.075),(51,7,9,1.5),(52,7,10,0.025),(53,7,11,0.012),(54,7,14,1.5),(55,8,4,1.2),(56,8,5,0.75),(57,8,6,0.75),(58,8,7,10),(59,8,8,0.075),(60,8,9,1.5),(61,8,10,0.025),(62,8,11,0.012),(63,8,15,0.15),(64,8,16,8),(65,9,4,1.2),(66,9,5,0.75),(67,9,6,0.75),(68,9,7,10),(69,9,8,0.075),(70,9,9,1.5),(71,9,10,0.025),(72,9,11,0.012),(73,9,13,2.5),(74,10,4,1.2),(75,10,5,0.75),(76,10,6,0.75),(77,10,7,10),(78,10,8,1.5),(79,10,10,0.025),(80,10,11,0.012);
/*!40000 ALTER TABLE `recetas_ingredientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitudes_materiales`
--

DROP TABLE IF EXISTS `solicitudes_materiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitudes_materiales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `cantidad` float NOT NULL,
  `unidad` varchar(20) NOT NULL,
  `precio_unitario` float NOT NULL,
  `proveedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedor_id` (`proveedor_id`),
  CONSTRAINT `solicitudes_materiales_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitudes_materiales`
--

LOCK TABLES `solicitudes_materiales` WRITE;
/*!40000 ALTER TABLE `solicitudes_materiales` DISABLE KEYS */;
INSERT INTO `solicitudes_materiales` VALUES (17,'Nutella',10,'kg',1200,3);
/*!40000 ALTER TABLE `solicitudes_materiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(200) NOT NULL,
  `name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'LuisGio51','gourmetCookies@gmail.com','scrypt:32768:8:1$AcRBIXD9AliUeYcO$f69f0f7684b744dde448d9b16d8e58b772635022f8713742d25b027ab581da5dbaab2f7d40fe3cc9a417159b35c46f92ed6d6f74ece1c6469e2f15acb10208cf','Luis','Claudio','Bernardo Cobos','4778283293','2025-04-12 02:05:18','empleado'),(3,'JorgeRag','jr960219@gmail.com','scrypt:32768:8:1$KgmZNAHRw0EXDfHO$1c1344acb4c09a4179d5c618eda1deb3e570a08b64f616a06066821dde316b86c1f5b6618b32704d09c684e6fa84eb820856bce5016959475fcbcf1fd5108760','Jorge','Rangel','Universidad','4776959595','2025-04-11 08:30:57','cliente'),(4,'LuisGerardo','lluis115@outlook.com','scrypt:32768:8:1$0nqEHl5RtNEKfHSa$1cc4cb0fe3cc737538574c36cd322e3810741bbece3f0351667bc42f0ca3a6f961b6c7095e618ce60d31c54e488d38cfcf8c46006f40316c8712dc8d01fd8d7c','Gerardo','Lopez','Universidad','4776959595','2025-04-12 02:01:46','cliente');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `idVenta` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `id_vendedor` int NOT NULL,
  `idPedido` int DEFAULT NULL,
  `fechaVenta` date NOT NULL,
  `precio` float NOT NULL,
  PRIMARY KEY (`idVenta`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_vendedor` (`id_vendedor`),
  KEY `idPedido` (`idPedido`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `user` (`id_user`),
  CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`id_vendedor`) REFERENCES `user` (`id_user`),
  CONSTRAINT `venta_ibfk_3` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`idPedido`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,NULL,1,NULL,'2025-04-11',270),(4,NULL,1,NULL,'2025-04-11',80),(5,4,1,1,'2025-04-11',80),(6,NULL,1,NULL,'2025-04-12',160),(7,4,1,2,'2025-04-12',180),(8,NULL,1,NULL,'2025-04-12',270);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-11 22:34:03
