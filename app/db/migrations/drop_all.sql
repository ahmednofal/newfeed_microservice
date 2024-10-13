SET FOREIGN_KEY_CHECKS = 0;  -- Disable foreign key checks

DROP TABLE IF EXISTS `comment`;
DROP TABLE IF EXISTS `share`;
DROP TABLE IF EXISTS `like_up`;
DROP TABLE IF EXISTS `post`;
DROP TABLE IF EXISTS `follow`;
DROP TABLE IF EXISTS `user`;

SET FOREIGN_KEY_CHECKS = 1;  -- Re-enable foreign key checks