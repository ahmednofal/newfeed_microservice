CREATE TABLE `user` (
  `id` BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `handle` CHAR(255) NOT NULL UNIQUE,
  `email` VARCHAR(255) NOT NULL,
  `password_hash` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `post` (
  `id` BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `author_id` BIGINT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  INDEX `idx_post_author` (`author_id`)
);

CREATE TABLE `like_up` (
  `liker_id` BIGINT NOT NULL,
  `post_id` BIGINT NOT NULL,
  PRIMARY KEY (`liker_id`, `post_id`),
  FOREIGN KEY (`liker_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
  INDEX `idx_like_liker` (`liker_id`),
  INDEX `idx_like_post` (`post_id`)
);

CREATE TABLE `share` (
  `id` BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `sharer_id` BIGINT NOT NULL,
  `post_id` BIGINT NOT NULL,
  FOREIGN KEY (`sharer_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
  INDEX `idx_share_sharer` (`sharer_id`),
  INDEX `idx_share_post` (`post_id`)
);

CREATE TABLE `follow` (
  `follower_id` BIGINT NOT NULL,
  `followed_id` BIGINT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`follower_id`, `followed_id`),
  FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  INDEX `idx_follow_follower` (`follower_id`),
  INDEX `idx_follow_followed` (`followed_id`)
);

CREATE TABLE `comment` (
  `id` BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `post_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
  INDEX `idx_comment_post` (`post_id`),
  INDEX `idx_comment_author` (`author_id`)
);
