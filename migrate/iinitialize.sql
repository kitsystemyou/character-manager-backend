-- Current Database: `charamane`

DROP DATABASE IF EXISTS `charamane`;

CREATE DATABASE `charamane` CHARACTER SET utf8mb4;

USE `charamane`;

-- Table structure for table `users`

DROP TABLE IF EXISTS `users`;

CREATE TABLE
    `users` (
        `id` char(32) NOT NULL COMMENT 'ユーザーID(UUID)',
        `user_name` char(50) NOT NULL COMMENT 'ユーザー名',
        `email` char(50) NOT NULL COMMENT 'メールアドレス',
        `login_type` char(20) NOT NULL COMMENT 'ログイン種別',
        `used_system` char(255) NULL COMMENT 'ゲームシステム利用実績',
        `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
        `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
        `delete_time` DATETIME NULL COMMENT '削除日時',
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB CHARSET = utf8mb4;

-- Table structure for table `characters`

DROP TABLE IF EXISTS `characters`;

CREATE TABLE
    `characters` (
        `id` int NOT NULL AUTO_INCREMENT COMMENT 'キャラクターID',
        `user_id` char(32) NOT NULL COMMENT 'ユーザーID(UUID)',
        `character_name` char(255) NOT NULL COMMENT 'PC名',
        `player_name` char(20) NOT NULL COMMENT 'PL名',
        `game_system` char(20) NOT NULL COMMENT 'ゲームシステム',
        `prof_img_path` char(50) NOT NULL COMMENT 'プロフ画像パス',
        `tags` char(255) NOT NULL COMMENT 'タグ(カンマ区切)',
        `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
        `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
        `delete_time` DATETIME NULL COMMENT '削除日時',
        PRIMARY KEY (`id`)
    ) ENGINE = InnoDB CHARSET = utf8mb4;

-- Table structure for table `coc_meta_info`

-- used in list card

DROP TABLE IF EXISTS `coc_meta_info`;

CREATE TABLE
    `coc_meta_info` (
        `character_id` int NOT NULL AUTO_INCREMENT COMMENT 'キャラクターID',
        `job` char(10) NULL COMMENT '職業',
        `sex` char(5) NULL COMMENT '性別',
        `age` char(5) NULL COMMENT '年齢',
        `height` char(5) NULL COMMENT '身長',
        `weight` char(5) NULL COMMENT '体重',
        `hair_color` char(20) NULL COMMENT '髪色',
        `eye_color` char(20) NULL COMMENT '目の色',
        `skin_color` char(20) NULL COMMENT '肌の色',
        `home_place` char(20) NULL COMMENT '出身',
        `mental_disorder` char(10) NULL COMMENT '精神的な障害',
        `edu_background` char(10) NULL COMMENT '学校・学位',
        `memo` char(100) NULL COMMENT 'メモ',
        FOREIGN KEY (`character_id`) REFERENCES characters (`id`)
    ) ENGINE = InnoDB CHARSET = utf8mb4;

-- Table structure for table `coc_status_parameters`

DROP TABLE IF EXISTS `coc_status_parameters`;

CREATE TABLE
    `coc_status_parameters` (
        `character_id` int NOT NULL AUTO_INCREMENT COMMENT 'キャラクターID',
        `str` int NULL COMMENT 'STR',
        `con` int NULL COMMENT 'CON',
        `pow` int NULL COMMENT 'POW',
        `dex` int NULL COMMENT 'DEX',
        `app` int NULL COMMENT 'APP',
        `size` int NULL COMMENT 'SIZE',
        `inte` int NULL COMMENT 'INT',
        `edu` int NULL COMMENT 'EDU',
        `hp` int NULL COMMENT 'HP',
        `mp` int NULL COMMENT 'MP',
        `init_san` int NULL COMMENT '初期正気度',
        `current_san` int NULL COMMENT '現在正気度',
        `idea` int NULL Comment 'アイデア',
        `knowledge` int NULL COMMENT '知識',
        `damage_bonus` int NULL COMMENT 'ダメージボーナス',
        `luck` int NULL COMMENT '幸運',
        `max_job_point` int NULL COMMENT '最大職業ポイント',
        `max_concern_point` int NULL COMMENT '最大興味ポイント',
        FOREIGN KEY (`character_id`) REFERENCES characters (`id`)
    ) ENGINE = InnoDB CHARSET = utf8mb4;

-- Table structure for table `coc_skills`

DROP TABLE IF EXISTS `coc_skills`;

CREATE TABLE
    `coc_skills` (
        `skill_id` int NOT NULL AUTO_INCREMENT COMMENT 'スキルID',
        `character_id` int NOT NULL COMMENT 'キャラクターID',
        `skill_name` char(50) NOT NULL COMMENT 'スキル名',
        `job_point` int NULL COMMENT '職業ポイント',
        `concern_point` int NULL COMMENT '興味ポイント',
        `grow` int NULL COMMENT '成長',
        `other` int NULL COMMENT 'その他',
        `skill_type` int NULL COMMENT '技能種別(基本/戦闘)',
        PRIMARY KEY (`skill_id`),
        CONSTRAINT `coc_skills_ibfk_1` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`)
    ) ENGINE = InnoDB CHARSET = utf8mb4;