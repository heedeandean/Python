
drop table if exists AlbumInfo;
CREATE TABLE `AlbumInfo` (
  `album_id` int(11) NOT NULL,
  `album_name` varchar(256) DEFAULT NULL,
  `agency` varchar(256) DEFAULT NULL,
  `rate` decimal(4,1) DEFAULT NULL,
  `album_likecnt` int(11) DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `singer` varchar(512) DEFAULT NULL,
  `release_date` varchar(31) DEFAULT NULL,
  PRIMARY KEY (`album_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists SongInfo;
CREATE TABLE `SongInfo` (
  `song_id` int(11) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `genre` varchar(50) DEFAULT NULL,
  `singer` varchar(512) DEFAULT NULL,
  `likecnt` int(11) DEFAULT NULL,
  `album_id` int(11) NOT NULL,
  `album_name` varchar(256) DEFAULT NULL,
  `release_date` varchar(31) DEFAULT NULL,
  PRIMARY KEY (`song_id`),
  KEY `fk_albumid_idx` (`album_id`),
  CONSTRAINT `fk_albumid` FOREIGN KEY (`album_id`) REFERENCES `AlbumInfo` (`album_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists DailyList;
CREATE TABLE `DailyList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rank` smallint(6) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `singer` varchar(512) DEFAULT NULL,
  `likecnt` int(11) DEFAULT NULL,
  `song_id` int(11) NOT NULL,
  `album_id` int(11) NOT NULL,
  `crawl_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_daily_songid_idx` (`song_id`),
  KEY `fk_album_idx` (`album_id`)
) ENGINE=InnoDB AUTO_INCREMENT=901 DEFAULT CHARSET=utf8;

drop table if exists Singer;
CREATE TABLE `Singer` (
  `singer_id` int(11) NOT NULL,
  `singer_name` varchar(126) DEFAULT NULL,
  PRIMARY KEY (`singer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists MappingSS;
CREATE TABLE `MappingSS` (
  `song_id` int(11) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `singer_name` varchar(126) DEFAULT NULL,
  `singer_id` int(11) NOT NULL,
  PRIMARY KEY (`song_id`,`singer_id`),
  KEY `fk_singerid_idx` (`singer_id`),
  CONSTRAINT `fk_singerid` FOREIGN KEY (`singer_id`) REFERENCES `Singer` (`singer_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_songid` FOREIGN KEY (`song_id`) REFERENCES `SongInfo` (`song_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

















