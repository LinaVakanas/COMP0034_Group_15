USE webapp;

CREATE TABLE IF NOT EXISTS user
(
    password_hash    VARBINARY(3)        NOT NULL,
    name             VARCHAR(32)         NOT NULL,
    surname          VARCHAR(32)         NOT NULL,
    bio              TEXT(140) DEFAULT NULL,
    email            VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
    active           BOOL      DEFAULT 0,
    profile_picture  BLOB      DEFAULT NULL,
    creation_date    DATETIME            NOT NULL,
    school_unique_ID tinyint             not null,
    user_type        tinyint             not null,
    user_id          tinyint             not null
);

CREATE TABLE IF NOT EXISTS mentee
(
    school_unique_ID tinyint not null,
    user_type        tinyint not null,
    user_id tinyint unique not null,
    paired_mentor    tinyint null,
    primary key (school_unique_ID, user_type, user_id)
);

CREATE TABLE IF NOT EXISTS PersonalInfoForm
(
    school_unique_ID    tinyint UNIQUE NOT NULL,
    user_type           tinyint        NOT NULL,
    user_id             tinyint UNIQUE NOT NULL,
    formID              tinyint        NOT NULL, #should it be student/mentor ID + form number?
    carer_email         varchar(255)   NOT NULL,
    carer_name          varchar(32)    NOT NULL,
    creation_date       date           NOT NULL,
    hobbies             varchar(255)   NULL,     #actually aren't they selecting an option? maybe itd be ints then?
    personality         varchar(32)    NOT NULL,
    medical_cond        varchar(255)   NULL,
    occupation_status   varchar(255)   NOT NULL,
    field               varchar(255)   NOT NULL,
    permission_to_share BOOL DEFAULT FALSE,
    primary key (school_unique_ID, user_type, user_id, formID),
    foreign key (school_unique_ID, user_type, user_id)
        references webapp.mentee (school_unique_ID, user_type, user_id)
);

CREATE TABLE IF NOT EXISTS PersonalIssues
(
    school_unique_ID    tinyint UNIQUE NOT NULL,
    user_type           tinyint        NOT NULL,
    user_id             tinyint UNIQUE NOT NULL,
    IssuesID tinyint DEFAULT 04, #we should set it a number?
    issue1 tinyint DEFAULT 0,
    issue2 tinyint DEFAULT 0,
    issue3 tinyint DEFAULT 0,
    issue4 tinyint DEFAULT 0,
    issue5 tinyint DEFAULT 0,
    issue6 tinyint DEFAULT 0,
    issue7 tinyint DEFAULT 0,
    issue8 tinyint DEFAULT 0,
    issue9 tinyint DEFAULT 0,
    primary key (school_unique_ID, user_type, user_id,IssuesID),
    foreign key (school_unique_ID, user_type, user_id)
        references webapp.mentee (school_unique_ID, user_type, user_id)
);

ALTER TABLE user
add foreign key (school_unique_ID, user_type, user_id)
        REFERENCES webapp.mentee (school_unique_ID, user_type, user_id)