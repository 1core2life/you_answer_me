
use USER;
 
CREATE TABLE challenger(
    idx    INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_idx    INT UNSIGNED NOT NULL,
    name    VARCHAR(20) NOT NULL,
    comment    VARCHAR(80),
    score    INT UNSIGNED NOT NULL,
    foreign key (user_idx) references  user(idx) on delete cascade) CHARSET=utf8;