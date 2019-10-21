-- MySQL dump 10.13  Distrib 5.7.22, for osx10.13 (x86_64)
--
-- Host: 127.0.0.1    Database: ppio
-- ------------------------------------------------------
-- Server version	5.7.23

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` char(56) NOT NULL,
  `type` tinyint(4) NOT NULL,
  `nonce` int(10) unsigned NOT NULL,
  `balance` char(30) CHARACTER SET ascii NOT NULL,
  `locked_balance` char(30) CHARACTER SET ascii NOT NULL,
  `spent_balance` char(30) CHARACTER SET ascii NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chunk_tracker`
--

DROP TABLE IF EXISTS `chunk_tracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chunk_tracker` (
  `id` char(32) NOT NULL,
  `chunk_type` tinyint(4) NOT NULL,
  `chunk_hash` char(64) NOT NULL,
  `chunk_size` int(11) NOT NULL,
  `miner_id` char(56) NOT NULL,
  `begin_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deposit_transaction`
--

DROP TABLE IF EXISTS `deposit_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deposit_transaction` (
  `id` char(64) NOT NULL,
  `account_id` char(56) NOT NULL,
  `amount` char(30) CHARACTER SET ascii NOT NULL,
  `begin_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` datetime DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `download_contract`
--

DROP TABLE IF EXISTS `download_contract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `download_contract` (
  `id` char(64) NOT NULL,
  `nonce` int(10) unsigned NOT NULL,
  `account_id` char(56) NOT NULL,
  `chunk_hash` char(64) NOT NULL,
  `chunk_size` int(11) NOT NULL,
  `chi_price` char(30) CHARACTER SET ascii NOT NULL,
  `funds` char(30) CHARACTER SET ascii NOT NULL,
  `begin_time` int(10) unsigned NOT NULL,
  `expire_time` int(10) unsigned NOT NULL,
  `end_time` int(10) unsigned NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `miner_capacity`
--

DROP TABLE IF EXISTS `miner_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `miner_capacity` (
  `miner_id` char(56) NOT NULL,
  `capacity` bigint(20) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`miner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `miner_contract`
--

DROP TABLE IF EXISTS `miner_contract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `miner_contract` (
  `id` char(64) NOT NULL,
  `seq` int(10) unsigned NOT NULL,
  `nonce` int(10) unsigned NOT NULL,
  `miner_id` char(56) NOT NULL,
  `rating` tinyint(4) NOT NULL DEFAULT '0',
  `total_space` bigint(20) NOT NULL,
  `used_space` bigint(20) NOT NULL DEFAULT '0',
  `left_space` bigint(20) NOT NULL,
  `earnings` char(30) CHARACTER SET ascii NOT NULL DEFAULT '0',
  `storage_chi_price` char(30) CHARACTER SET ascii NOT NULL,
  `download_chi_price` char(30) CHARACTER SET ascii NOT NULL,
  `begin_time` int(10) unsigned NOT NULL,
  `leave_time` int(10) unsigned NOT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `peer`
--

DROP TABLE IF EXISTS `peer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `peer` (
  `account_id` char(56) NOT NULL,
  `peer_info` blob NOT NULL,
  `keep_alive_time` int(10) unsigned NOT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proof_lpoc`
--

DROP TABLE IF EXISTS `proof_lpoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proof_lpoc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `verifier_id` char(56) NOT NULL,
  `miner_id` char(56) NOT NULL,
  `capacity` bigint(20) NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proof_post`
--

DROP TABLE IF EXISTS `proof_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proof_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `verifier_id` char(56) NOT NULL,
  `miner_id` char(56) NOT NULL,
  `chunk_hash` char(64) NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proof_pot`
--

DROP TABLE IF EXISTS `proof_pot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proof_pot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `verifier_id` char(56) NOT NULL,
  `miner_id` char(56) NOT NULL,
  `contract_id` char(64) NOT NULL,
  `piece_num` int(11) NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proof_rep`
--

DROP TABLE IF EXISTS `proof_rep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proof_rep` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `verifier_id` char(56) NOT NULL,
  `miner_id` char(56) NOT NULL,
  `chunk_hash` char(64) NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `storage_contract`
--

DROP TABLE IF EXISTS `storage_contract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storage_contract` (
  `id` char(64) NOT NULL,
  `nonce` int(10) unsigned NOT NULL,
  `payer_id` char(56) NOT NULL,
  `user_id` char(56) NOT NULL,
  `miner_id` char(56) NOT NULL,
  `chunk_hash` char(64) NOT NULL,
  `chunk_size` int(11) NOT NULL,
  `user_chi_price` char(30) CHARACTER SET ascii NOT NULL,
  `miner_chi_price` char(30) CHARACTER SET ascii NOT NULL,
  `user_funds` char(30) CHARACTER SET ascii NOT NULL,
  `miner_pledges` char(30) CHARACTER SET ascii NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `begin_time` int(10) unsigned NOT NULL,
  `settlement_time` int(10) unsigned NOT NULL DEFAULT '0',
  `expire_time` int(10) unsigned NOT NULL,
  `end_time` int(10) unsigned NOT NULL DEFAULT '0',
  `end_event` varchar(20) DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transfer_transaction`
--

DROP TABLE IF EXISTS `transfer_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transfer_transaction` (
  `id` char(64) NOT NULL,
  `action` tinyint(4) NOT NULL,
  `from_account_id` char(56) NOT NULL,
  `to_account_id` char(56) NOT NULL,
  `amount` char(30) CHARACTER SET ascii NOT NULL,
  `comment` varchar(100) DEFAULT NULL,
  `begin_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` datetime DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-10 22:24:27
