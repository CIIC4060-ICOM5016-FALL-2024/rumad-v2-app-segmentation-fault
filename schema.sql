CREATE TABLE IF NOT EXISTS "requisite" (

);

CREATE TABLE IF NOT EXISTS "class" (

);

CREATE TABLE IF NOT EXISTS "syllabus" (

);

CREATE TABLE IF NOT EXISTS "section" (

);

CREATE TABLE IF NOT EXISTS "room" (
    "rid" SERIAL PRIMARY KEY,
    "building" VARCHAR(255),
    "room_number" VARCHAR,
    "capacity" INTEGER
);

CREATE TABLE IF NOT EXISTS "meeting" (
    "mid" SERIAL PRIMARY KEY,
    "ccode" VARCHAR(10),
    "starttime" TIMESTAMP,
    "endtime" TIMESTAMP,
    "cdays" VARCHAR(5) 
);