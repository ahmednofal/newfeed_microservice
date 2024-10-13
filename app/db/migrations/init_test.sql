SET FOREIGN_KEY_CHECKS = 0;  -- Disable foreign key checks

TRUNCATE TABLE `comment`;
TRUNCATE TABLE `share`;
TRUNCATE TABLE `like_up`;
TRUNCATE TABLE `post`;
TRUNCATE TABLE `follow`;
TRUNCATE TABLE `user`;

SET FOREIGN_KEY_CHECKS = 1;  -- Re-enable foreign key checks

-- Populating the user table
INSERT INTO `user` (`handle`, `email`, `password_hash`, `created_at`) VALUES
('user1', 'user1@example.com', 'hash1', NOW()),
('user2', 'user2@example.com', 'hash2', NOW()),
('user3', 'user3@example.com', 'hash3', NOW()),
('user4', 'user4@example.com', 'hash4', NOW());

-- Populating the post table
INSERT INTO `post` (`content`, `author_id`, `created_at`, `is_deleted`) VALUES
('This is the first post!', 1, NOW(), FALSE),
('This is the second post!', 1, NOW(), FALSE),
('This is the third post!', 2, NOW(), FALSE),
('This is the fourth post!', 3, NOW(), FALSE),
('This is a deleted post!', 2, NOW(), TRUE);

-- Populating the like_up table
INSERT INTO `like_up` (`liker_id`, `post_id`) VALUES
(1, 1),
(2, 1),
(2, 3),
(3, 2),
(4, 1),
(1, 2),
(2, 2);

-- Populating the share table
INSERT INTO `share` (`sharer_id`, `post_id`) VALUES
(1, 3),
(2, 1),
(3, 2),
(4, 1);

-- Populating the follow table
INSERT INTO `follow` (`follower_id`, `followed_id`, `created_at`) VALUES
(1, 2, NOW()),
(1, 3, NOW()),
(2, 1, NOW()),
(3, 4, NOW()),
(4, 1, NOW()),
(4, 2, NOW());

-- Populating the comment table
INSERT INTO `comment` (`post_id`, `author_id`, `content`, `created_at`) VALUES
(1, 2, 'Great post!', NOW()),
(1, 3, 'Thanks for sharing!', NOW()),
(2, 1, 'Interesting thoughts.', NOW()),
(3, 1, 'I completely agree!', NOW()),
(3, 4, 'Nice insights!', NOW()),
(4, 2, 'Could you elaborate more?', NOW());
