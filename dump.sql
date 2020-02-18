-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: InternshipProject
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.18.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Accostage`
--

DROP TABLE IF EXISTS `Accostage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Accostage` (
  `id_accostage` int(11) NOT NULL AUTO_INCREMENT,
  `nom_navire` varchar(100) DEFAULT NULL,
  `nbr_de_mains` char(1) DEFAULT NULL,
  `tonnage_navire` varchar(8) DEFAULT NULL,
  `ie_navire` varchar(8) DEFAULT NULL,
  `point_metrique` varchar(3) DEFAULT NULL,
  `date_accostage` varchar(12) DEFAULT NULL,
  `shift_de_depart` char(1) DEFAULT NULL,
  PRIMARY KEY (`id_accostage`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Accostage`
--

LOCK TABLES `Accostage` WRITE;
/*!40000 ALTER TABLE `Accostage` DISABLE KEYS */;
INSERT INTO `Accostage` VALUES (43,'Amberly Castle | MAERSK | 170 | 12 | USA | Porte Conteneurs','1','','120/250','5','10/12/2019','1'),(44,'GAMA SUD | GAMA | 170 | 58 | Taiwan | Porte Conteneur','1','','120/280','6','11/12/2019','2'),(45,'GAMA SUD | GAMA | 170 | 58 | Taiwan | Porte Conteneur','1','','120/280','6','11/12/2019','1');
/*!40000 ALTER TABLE `Accostage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Navire`
--

DROP TABLE IF EXISTS `Navire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Navire` (
  `id_navire` int(11) NOT NULL AUTO_INCREMENT,
  `nom_navire` varchar(100) DEFAULT NULL,
  `agent_navire` varchar(100) DEFAULT NULL,
  `loa_navire` varchar(100) DEFAULT NULL,
  `tirant_eau_navire` varchar(100) DEFAULT NULL,
  `pays_navire` varchar(100) DEFAULT NULL,
  `type_navire` varchar(100) DEFAULT NULL,
  `couleur_navire` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_navire`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Navire`
--

LOCK TABLES `Navire` WRITE;
/*!40000 ALTER TABLE `Navire` DISABLE KEYS */;
INSERT INTO `Navire` VALUES (6,'PERSUS J','PERSUS','170','20','Swede','Porte Conteneur','#4e9a06'),(8,'MED NORDIC NA','MED NORDIC','170','15','Denmark','Vraq','#ad7fa8'),(9,'GAMA SUD','GAMA','170','58','Taiwan','Porte Conteneur','#888a85'),(10,'Amberly Castle','MAERSK','170','12','USA','Porte Conteneurs','#ce5c00'),(11,'Gold Coast BIR','Gold','156','22','EU','Porte Conteneurs','#c17d11'),(12,'X Y Z','MSC','170','20','EU','Porte Conteneurs','#ce5c00'),(13,'XYX','X','170','22','US','Porte Conteneurs','#f57900'),(14,'Amber Castle','AMRESK','170','5','SWEDE','Porte Conteneurs','#f61a1a'),(15,'Amberly Castle','MAERSK','170','23','SWEDE','Porte Conteneurs','#73d216'),(16,'efeqfe','fefef','efef','fefe','fefef','Porte Conteneurs','');
/*!40000 ALTER TABLE `Navire` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-11  0:44:12
