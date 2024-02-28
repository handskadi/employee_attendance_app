-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: eap
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `attendance_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `attendance_date` date NOT NULL,
  `day_shift_hours` decimal(10,0) DEFAULT NULL,
  `night_shift_hours` decimal(10,0) DEFAULT NULL,
  `hours_worked` decimal(10,0) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`attendance_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (9,6,'2024-02-21',2,5,7,'He is Hamma'),(10,4,'2024-02-04',2,1,3,'Lbghli lawah nbeg'),(11,4,'2024-02-22',2,1,3,'lkabs'),(12,3,'2024-02-06',1,2,3,'Kasoul'),(13,22,'2024-02-21',8,8,16,'DR.'),(14,6,'2024-02-23',4,4,8,'Mecanic'),(15,4,'2024-02-25',2,1,3,'lok'),(16,3,'2024-02-16',1,4,5,'Tui Project'),(17,3,'2024-02-27',5,6,11,'Travel Agency DMC'),(18,5,'2024-02-02',2,5,7,'updated 2487878wafa'),(19,4,'2024-02-02',8,0,8,'updated :)'),(20,2,'2024-02-01',1,1,2,'added now1477'),(21,5,'2024-02-06',5,5,10,'here'),(22,6,'2024-02-01',1,4,5,'here77'),(23,28,'2024-02-28',8,4,12,'orss'),(24,1,'2024-02-28',4,9,13,'zdddd'),(25,1,'2024-02-26',8,4,12,'this is added right now');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `hire_date` date NOT NULL,
  `end_employment` date NOT NULL,
  `manager_id` int DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `role` enum('project_manager','general_manager','employee') NOT NULL DEFAULT 'employee',
  `image_filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'default.png',
  PRIMARY KEY (`employee_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,1,'2020-01-01','2300-01-01',2,1,'Wafa','Marouani','general_manager','wafa.jpg'),(2,2,'2020-01-01','2300-01-01',2,1,'Mohamed','KADI','project_manager','mk-modified.jpg'),(3,3,'2024-01-23','2030-01-01',2,1,'Azzedine','Nait Azizi','employee','default.png'),(4,4,'2024-01-01','2028-03-06',2,1,'Aimad','Abdelghani','employee','aimad.png'),(5,5,'2024-01-01','2030-01-01',2,1,'Amine','Kaddi','employee','amine.jpg'),(6,6,'2027-10-23','2027-01-16',2,9,'Karim','El-Khadiri','project_manager','default.png'),(7,7,'2023-12-23','2035-01-01',8,2,'Zizo','Hammot','employee','nazihelkhadiri.jpg'),(8,8,'2024-02-03','2035-01-01',1,2,'Mohamed','Abdelghani','project_manager','belhaj.jpg'),(22,36,'2024-02-02','2024-03-06',8,1,'Sana','KADI','employee','default.png'),(23,37,'2024-02-15','2024-03-30',2,9,'Santwa','KADI','employee','sanakadi.jpg'),(24,38,'2024-02-02','2024-03-09',2,1,'Ahmed','KADI','employee','ahmedkadi.jpg'),(25,39,'2011-01-01','2050-02-02',2,1,'Faima','KADI','general_manager','fatimakadi.jpg'),(26,41,'2023-06-05','2048-04-02',2,1,'Abdelghani ','Azza','employee','mohamedabdelghani.jpg'),(27,42,'2022-01-02','2029-02-04',6,7,'John','Doh','employee','achraf.jpg'),(28,43,'2024-02-28','2024-02-29',8,7,'Samir','Wadot','employee','img_avatar1.png'),(41,62,'0003-12-22','0001-11-11',6,14,'Achraf','Hakimi','project_manager','default.png');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) NOT NULL,
  `is_active` smallint NOT NULL,
  `description` text,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'Mkweb Project',1,'Web development and Design Project'),(2,'QA Project',1,'WaMO Testing Project'),(7,'TIN Pro Project',1,'Tinghir Building construction'),(8,'Nike ',0,'Nike Project In Tinghir '),(9,'Project Z',1,'Project Z desc'),(10,'Marrakech AFTL',0,'Plants\' Project'),(11,'Plant\'s Project',0,'Export Plants and Make it Amazing '),(13,'Ghazala Project',0,'Ghazala Camp Project'),(14,'ALx Project',1,'SWE Program'),(15,'ETS Travel',1,'DMC & Travel Agency in Marrakech Renovation '),(16,'Aslmd',0,'Teaching German for Non Germans');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'wmarouani','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','wafa@marouani.com'),(2,'mohamedkadi','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','moha@kadi.com'),(3,'azzedine','aziz#2023','la@aziz.com'),(4,'Aimad','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','la3moum@saraf.com'),(5,'mejo','mejo#2023','abdel@faris.com'),(6,'krimo','krimo#2023','krimo@hamma.com'),(7,'zizohama','nazih#2023','nazih@hamma.com'),(8,'belhaj','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','moh@baqaddi.com'),(36,'sana','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','sanati@gmail.com'),(37,'sanati','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','sana@gmail.com'),(38,'ahmd','$2b$12$cVoICDsgjPlaiGvF6jfVWODkFcseJ3HuQYjBsiO/c1kiBe6NfZp8O','daki@ahmed.com'),(39,'bader','$2b$12$3WW0N3tGlJxUENmrtjmjHuMRBoy4CRmIs18fYPk6N54tpWwq2FEnW','pedro@rj.d'),(41,'bal','$2b$12$dGSzl0SpcyglrBZ7CwfWyOjxHsx9iXPNY6UswZbyryfkhfe4uPKA6','kk@kj.x'),(42,'jwj','$2b$12$g.P6bt9bY3OJjA8sWta5E.0NrrccxEiJ9GKrmgOehWjaBefIFHXSm','m@k.com'),(43,'samor','$2b$12$JeCxzf3kQDU6qXi1NBWWf.ovBt41ryKjh.Xj9a1LBR7WmTckjsQ9u','samir@wadot.com'),(62,'achrafo','$2b$12$7A2jq4f7QUKom7Mss83taOO3OEsUK9v6QJduUsGZ1L9pwQrhsoDDW','hakimi@psg.com');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-28 19:41:51
