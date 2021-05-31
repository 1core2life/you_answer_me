
use USER;
 
CREATE TABLE user_question(
    idx    INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    question_idx    INT UNSIGNED NOT NULL,
    user_idx    INT UNSIGNED NOT NULL,
    answer    INT UNSIGNED NOT NULL,
    foreign key (user_idx) references  user(idx) on delete cascade) CHARSET=utf8;