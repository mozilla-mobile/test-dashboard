-- MySQL dump 10.13  Distrib 8.0.22, for osx10.16 (x86_64)
--
-- Host: 127.0.0.1    Database: staging 
-- ------------------------------------------------------
-- Server version	5.7.33-google-log

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
-- Current Database: `staging`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `staging` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `staging`;

--
-- Table structure for table `test_coverage`
--

DROP TABLE IF EXISTS `test_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projects_id` int(11) NOT NULL, 
  `test_suites_id` int(11) NOT NULL, 
  `test_automation_flags_id` int(11) NOT NULL, 
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY(`projects_id`) REFERENCES projects(`id`))
  FOREIGN KEY(`test_suites_id`) REFERENCES test_suites(`id`))
  FOREIGN KEY(`test_automation_flags_id`) REFERENCES test_automation_flags(`id`))
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`)
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test_suites`
--

DROP TABLE IF EXISTS `test_suites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_suites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_suites_type` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`)
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test_automation_flags`
--

DROP TABLE IF EXISTS `test_automation_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_automation_flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flag` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`)
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`)
/*!40101 SET character_set_client = @saved_cs_client */;




--
-- Table structure for table `github_test`
--

DROP TABLE IF EXISTS `github_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `github_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `open` int(11) NOT NULL,
  `closed` int(11) NOT NULL,
  `label` varchar(50) DEFAULT NULL,
  `project_name` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `testrail_test_coverage`
--

DROP TABLE IF EXISTS `testrail_test_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testrail_test_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projects_id` int(11) NOT NULL, 
  `suite` varchar(100) DEFAULT NULL,
  `automation_state` varchar(100) DEFAULT NULL,
  `case_count` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY(`projects_id`) REFERENCES projects(`id`))
) ENGINE=InnoDB AUTO_INCREMENT=1671 DEFAULT CHARSET=utf8;

--
-- Table structure for table `demo`
--

DROP TABLE IF EXISTS `demo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `artist` varchar(255) DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;


/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-17 13:47:56

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES ('fenix', 'focus-android', 'firefox-ios', 'focus-ios', 'android-components', 'reference-browser');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `test_suites`
--

LOCK TABLES `test_suites` WRITE;
/*!40000 ALTER TABLE `test_suites` DISABLE KEYS */;
INSERT INTO `test_suites` VALUES ('Full Functional', 'Smoke', 'Accessibility', 'L10N', 'Telemetry', 'Search', 'Top Sites');
/*!40000 ALTER TABLE `test_suites` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `test_automation_flags`
--

LOCK TABLES `test_automation_flags` WRITE;
/*!40000 ALTER TABLE `test_automation_flags` DISABLE KEYS */;
INSERT INTO `test_automation_flags` VALUES ('untriaged', 'suitable', 'unsuitable', 'completed', 'disabled');
/*!40000 ALTER TABLE `test_automation_flags` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Dumping data for table `demo`
--

LOCK TABLES `demo` WRITE;
/*!40000 ALTER TABLE `demo` DISABLE KEYS */;
INSERT INTO `demo` VALUES (1,'Say so','Doja Cat','HipHop','2021-04-12 15:09:49'),(2,'Rockstar','Dababy','rap','2021-04-12 15:09:49'),(3,'God\'s plan','Drake','Rap','2021-04-12 15:09:49'),(4,'My Record','Richard P.','rock','2021-04-12 15:09:49'),(5,'Let It Be','Beatles','Rock','2021-04-12 15:09:49'),(6,'Obla di','Beatles','Rock','2021-04-12 15:09:49'),(7,'Radio Clash','The Clash','Punk','2021-04-12 15:09:49');
/*!40000 ALTER TABLE `demo` ENABLE KEYS */;
UNLOCK TABLES;
