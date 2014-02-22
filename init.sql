CREATE DATABASE `python` /*!40100 DEFAULT CHARACTER SET latin1 */;
CREATE TABLE `wx_test` (
      `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
      `title` varchar(64) DEFAULT '',
      `url` varchar(255) NOT NULL DEFAULT '' COMMENT 'URL',
      KEY `id_index` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
