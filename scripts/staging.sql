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
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testrail_id` int(11) NOT NULL,
  `testrail_functional_test_suite_id` int(11) NOT NULL,
  `project_name_abbrev` varchar(25) NOT NULL,
  `project_name` varchar(75) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `test_suites`
--

DROP TABLE IF EXISTS `test_suites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_suites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_suite_abbrev` varchar(25) NOT NULL,
  `test_suite` varchar(75) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test_sub_suites`
--

DROP TABLE IF EXISTS `test_sub_suites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_sub_suites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testrail_id` int(11) NOT NULL,
  `test_sub_suite_abbrev` varchar(25) NOT NULL,
  `test_sub_suite` varchar(75) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `test_automation_status`
--

DROP TABLE IF EXISTS `test_automation_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_automation_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testrail_id` int(11) NOT NULL,
  `status` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `test_automation_coverage`
--

DROP TABLE IF EXISTS `test_automation_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_automation_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testrail_id` int(11) NOT NULL,
  `coverage` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `report_test_coverage`
--

DROP TABLE IF EXISTS `report_test_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_test_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projects_id` int(11) NOT NULL, 
  `test_suites_id` int(11) NOT NULL DEFAULT 1, 
  `test_sub_suites_id` int(11) NOT NULL DEFAULT 1, 
  `test_automation_status_id` int(11) NOT NULL, 
  `test_automation_coverage_id` int(11) NOT NULL, 
  `test_count` int(11) NOT NULL DEFAULT 0, 
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY(`projects_id`) REFERENCES projects(`id`),
  FOREIGN KEY(`test_suites_id`) REFERENCES test_suites(`id`),
  FOREIGN KEY(`test_sub_suites_id`) REFERENCES test_sub_suites(`id`),
  FOREIGN KEY(`test_automation_status_id`) REFERENCES test_automation_status(`id`),
  FOREIGN KEY(`test_automation_coverage_id`) REFERENCES test_automation_coverage(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;



/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

--
-- data for reference table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` (`testrail_id`, `testrail_functional_test_suite_id`, `project_name_abbrev`, `project_name`) VALUES (59, 3192, 'fenix', 'Fenix Browser'), (48, 1028, 'focus-android', 'Focus for Android'), (14, 1157, 'firefox-ios', 'Firefox for iOS'), (27, 5291, 'focus-ios', 'Focus for iOS'), (58, 3179, 'reference-browser', 'Reference Browser');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;


--
-- data for reference table `test_suites`
--

LOCK TABLES `test_suites` WRITE;
/*!40000 ALTER TABLE `test_suites` DISABLE KEYS */;
INSERT INTO `test_suites` (`test_suite_abbrev`, `test_suite`) VALUES ('functional', 'Full Functional Tests Suite');
/*!40000 ALTER TABLE `test_suites` ENABLE KEYS */;
UNLOCK TABLES;


--
-- data for reference table `test_sub_suites`
--

LOCK TABLES `test_sub_suites` WRITE;
/*!40000 ALTER TABLE `test_sub_suites` DISABLE KEYS */;
INSERT INTO `test_sub_suites` (`testrail_id`, `test_sub_suite_abbrev`, `test_sub_suite`) VALUES (0, 'functional', 'Functional'), (1, 'smoke', 'Smoke & Sanity'), (2, 'accessibility', 'Accessibility'), (3, 'l10n', 'L10n'), (4, 'security', 'Security');
/*!40000 ALTER TABLE `test_sub_suites` ENABLE KEYS */;
UNLOCK TABLES;


--
-- data for reference table `test_automation_status`
--

LOCK TABLES `test_automation_status` WRITE;
/*!40000 ALTER TABLE `test_automation_status` DISABLE KEYS */;
INSERT INTO `test_automation_status`(`testrail_id`, `status`) VALUES (1, 'Untriaged'), (2, 'Suitable'), (3, 'Unsuitable'), (4, 'Completed'), (5, 'Disabled');
/*!40000 ALTER TABLE `test_automation_status` ENABLE KEYS */;
UNLOCK TABLES;


--
-- data for reference table `test_automation_coverage`
--

LOCK TABLES `test_automation_coverage` WRITE;
/*!40000 ALTER TABLE `test_automation_coverage` DISABLE KEYS */;
INSERT INTO `test_automation_coverage`(`testrail_id`, `coverage`) VALUES (1, 'None'), (2, 'Partial'), (3, 'Full');
/*!40000 ALTER TABLE `test_automation_coverage` ENABLE KEYS */;
UNLOCK TABLES;


