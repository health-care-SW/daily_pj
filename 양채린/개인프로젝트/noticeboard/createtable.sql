SET foreign_key_checks = 0;
drop table if exists question;
create table question (
	id integer primary key auto_increment,
    create_date datetime not null,
    user_id integer,
    entpName varchar(50),
    itemName varchar(50),
    efcyQesitm varchar(1000),
    useMethodQesitm varchar(1000),
    atpnQesitm varchar(1000),
    depositMethodQesitm varchar(1000)
    );


drop table if exists answer;
create table answer (
	id integer primary key auto_increment,
    question_id integer,
    content varchar(10000) not null,
    create_date datetime not null,
    user_id integer,
    modify_date datetime null
);

drop table if exists user;
create table user (
	id integer primary key auto_increment,
    username varchar(150) unique not null,
    password varchar(200) not null,
    email varchar(120) unique not null
);

drop table if exists comment;
create table comment ( 
	id integer primary key auto_increment,
    user_id integer,
    content varchar(10000),
    create_date datetime not null,
    modify_date datetime null,
    question_id integer,
    answer_id integer
);
        

-- ----------------------------

alter table answer
add constraint fk_answer1
foreign key (question_id) references question (id)
on delete cascade;

alter table answer
add constraint fk_answer2
foreign key (user_id) references user (id)
on delete cascade;
  
-- ----------------------------
        
alter table question
add constraint fk_question
foreign key (user_id) references user (id)
on delete cascade;

-- ----------------------------

alter table comment
add constraint fk_comment1
foreign key (user_id) references user (id)
on delete cascade;

alter table comment
add constraint fk_comment2
foreign key (question_id) references question (id)
on delete cascade;

alter table comment
add constraint fk_comment3
foreign key (answer_id) references answer (id)
on delete cascade;



select * from question;
select * from answer;
select * from user;
select * from comment;

SET foreign_key_checks = 1;