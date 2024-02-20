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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (1,3,'2024-02-17',8,0,8,'Regular work day'),(2,4,'2024-02-17',8,2,10,'Regular work day'),(3,5,'2024-02-17',8,0,8,'Regular work day'),(4,6,'2024-02-17',5,4,9,'Regular work day'),(5,7,'2024-02-17',8,0,8,'Regular work day');
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
  `image_filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`employee_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,1,'2020-01-01','2300-01-01',NULL,NULL,'Wafa','Marouani','general_manager','wafa.jpg'),(2,2,'2020-01-01','2300-01-01',1,1,'Mohamed','KADI','project_manager','mk.jpg'),(3,3,'2024-01-23','2030-01-01',2,1,'Azzedine','Nait Azizi','employee','default.png'),(4,4,'2024-01-01','2028-03-06',2,1,'Aimad','Abdelghani','employee','aimad.png'),(5,5,'2024-01-01','2030-01-01',2,1,'Abdel Moujoud','Faris','employee','default.png'),(6,6,'2023-12-23','2028-05-16',8,2,'Karim','El Khadiri','employee','default.png'),(7,7,'2023-12-23','2035-01-01',8,2,'Nazih','Hamma','employee','nazih.jpg'),(8,8,'2024-02-03','2035-01-01',1,2,'Mohamed','Abdelghani','project_manager','belhaj.jpg'),(22,36,'2024-02-02','2024-03-06',8,1,'Sana','KADI','employee','default.png'),(23,37,'2024-02-15','2024-03-30',2,1,'Sana','KADI','general_manager','sanakadi.jpg');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'Mkweb Project',1,'Web development and Design Project'),(2,'QA Project',1,'WaMO Testing Project'),(7,'TIN Pro Project',1,'Tinghir Building construction'),(8,'test project',0,'tes descript'),(9,'Project Z',1,'Project Z desc');
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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'wmarouani','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','wafa@marouani.com'),(2,'mohamedkadi','$2b$12$CbTGKGqaN4TTADImUtKGP.9zu7.2PnutyJ3O8k.B8yy5Por/4JpKS','moha@kadi.com'),(3,'azzedine','aziz#2023','la@aziz.com'),(4,'Aimad','la3mom#2023','la3moum@saraf.com'),(5,'mejo','mejo#2023','abdel@faris.com'),(6,'krimo','krimo#2023','krimo@hamma.com'),(7,'zizohama','nazih#2023','nazih@hamma.com'),(8,'belhaj','belhaj#2023','moh@baqaddi.com'),(36,'sana','$2b$12$QkuFOklMc8uUhcyCCRXqf.o6cemgDtlXja3V8KKE1a0vaHPWC4nz.','sanati@gmail.com'),(37,'sanati','$2b$12$QjT9Os0Cy2grXVlfyY8LBOw4tIWw36jweKS1MQslyYUKDsMqPezTu','sana@gmail.com');
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

-- Dump completed on 2024-02-20 14:47:56
