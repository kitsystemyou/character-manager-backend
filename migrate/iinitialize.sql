--
-- Current Database: `charamane`
--

DROP DATABASE IF EXISTS `charamane`;
CREATE DATABASE `charamane` DEFAULT CHARACTER SET utf8mb4;
USE `charamane`;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uuid` char(32) NOT NULL DEFAULT '',
  `username` char(50) NOT NULL DEFAULT '',
  `email` char(50) NOT NULL DEFAULT '',
  `login_type` char(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `characters`
--

DROP TABLE IF EXISTS `characters`;
CREATE TABLE `characters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` char(3) NOT NULL DEFAULT '',
  `scenario_system` char(3) NOT NULL DEFAULT '',
  `prof_img_path` char(3) NOT NULL DEFAULT '',
  `tags` char(3) NOT NULL DEFAULT '',
  `job` char(3) NOT NULL DEFAULT '',
  `age` char(3) NOT NULL DEFAULT '',
  `sex` char(3) NOT NULL DEFAULT '',
  `height` char(3) NOT NULL DEFAULT '',
  `weight` char(3) NOT NULL DEFAULT '',
  `hair_color` char(3) NOT NULL DEFAULT '',
  `eye_color` char(3) NOT NULL DEFAULT '',
  `skin_color` char(3) NOT NULL DEFAULT '',
  `home_place` char(3) NOT NULL DEFAULT '',
  `con` int DEFAULT NULL,
  `pow` int DEFAULT NULL,
  `dex` int DEFAULT NULL,
  `app` int DEFAULT NULL,
  `size` int DEFAULT NULL,
  `int` int DEFAULT NULL,
  `edu` int DEFAULT NULL,
  `Capital` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `basic_parameters`
--

DROP TABLE IF EXISTS `basic_parameters`;
CREATE TABLE `basic_parameters` (
  `character_id` int DEFAULT NULL,
  `hp` int DEFAULT NULL,
  `mp` int DEFAULT NULL,
  `max_san` int DEFAULT NULL,
  `current_san` int DEFAULT NULL,
  `ide` int DEFAULT NULL,
  `luck` int DEFAULT NULL,
  `damage_bonus` int DEFAULT NULL,
  `max_job_point` int DEFAULT NULL,
  `remain_job_point` int DEFAULT NULL,
  `max_concern_point` int DEFAULT NULL,
  `remain_concern_point` int DEFAULT NULL,
  CONSTRAINT `basic_skills_ibfk_1` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `coc_skills`
--

DROP TABLE IF EXISTS `coc_skills`;
CREATE TABLE `coc_skills` (
  `character_id` int DEFAULT NULL,
  `skill_id` int NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL DEFAULT '',
  `init` int DEFAULT NULL,
  `job_point` int DEFAULT NULL,
  `concern_point` int DEFAULT NULL,
  `grow` int DEFAULT NULL,
  `other` int DEFAULT NULL,
  `type` int DEFAULT NULL,
  PRIMARY KEY (`skill_id`),
  CONSTRAINT `coc_skills_ibfk_1` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `other_skills`
--

DROP TABLE IF EXISTS `other_skills`;
CREATE TABLE `other_skills` (
  `character_id` int DEFAULT NULL,
  `name` char(3) NOT NULL DEFAULT '',
  CONSTRAINT `other_skills_ibfk_1` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;