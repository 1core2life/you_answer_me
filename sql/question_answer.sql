
use USER;
 
CREATE TABLE question_answer(
    idx    INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    question_idx    INT UNSIGNED NOT NULL,
    content    VARCHAR(40) NOT NULL,
    foreign key (question_idx) references  question(idx) on delete cascade) CHARSET=utf8;