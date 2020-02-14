use webapp;

create table if not exists mentee
(
    school_unique_ID tinyint not null,
    user_type        tinyint not null,
    user_id          tinyint not null,
    paired_mentor    tinyint null,
    primary key (school_unique_ID, user_type, user_id),
    constraint user_id
        unique (user_id)
);

create table if not exists personalinfoform
(
    school_unique_ID    tinyint              not null,
    user_type           tinyint              not null,
    user_id             tinyint              not null,
    formID              tinyint              not null,
    carer_email         varchar(255)         not null,
    carer_name          varchar(32)          not null,
    creation_date       date                 not null,
    hobbies             varchar(255)         null,
    personality         varchar(32)          not null,
    medical_cond        varchar(255)         null,
    occupation_status   varchar(255)         not null,
    field               varchar(255)         not null,
    permission_to_share tinyint(1) default 0,
    constraint user_id
        unique (user_id),
    constraint personalinfoform_key
        foreign key (school_unique_ID, user_type, user_id) references mentee (school_unique_ID, user_type, user_id)
);

create table if not exists personalissues
(
    school_unique_ID tinyint           not null,
    user_type        tinyint           not null,
    user_id          tinyint           not null,
    IssuesID         tinyint default 4 not null,
    issue1           tinyint default 0 null,
    issue2           tinyint default 0 null,
    issue3           tinyint default 0 null,
    issue4           tinyint default 0 null,
    issue5           tinyint default 0 null,
    issue6           tinyint default 0 null,
    issue7           tinyint default 0 null,
    issue8           tinyint default 0 null,
    issue9           tinyint default 0 null,
    constraint user_id
        unique (user_id),
    constraint personalissues_key
        foreign key (school_unique_ID, user_type, user_id) references mentee (school_unique_ID, user_type, user_id)
);

create table if not exists user
(
    password_hash    varbinary(3)         not null,
    name             varchar(32)          not null,
    surname          varchar(32)          not null,
    bio              text                 null,
    email            varchar(255)         not null,
    active           tinyint(1) default 0 null,
    profile_picture  blob                 null,
    creation_date    datetime             not null,
    school_unique_ID tinyint              not null,
    user_type        tinyint              not null,
    user_id          tinyint              not null,
    constraint email
        unique (email),
        primary key (email),
    constraint user_key
        foreign key (school_unique_ID, user_type, user_id) references mentee (school_unique_ID, user_type, user_id)
);




