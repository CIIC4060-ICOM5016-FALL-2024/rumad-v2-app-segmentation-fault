CREATE TABLE IF NOT EXISTS "requisite" (

);

CREATE TABLE IF NOT EXISTS "class" (

);

CREATE TABLE IF NOT EXISTS "syllabus" (

);

CREATE TABLE IF NOT EXISTS "section" (
  "sid" SERIAL PRIMARY KEY,
  "roomid" INTEGER,
  "cid" INTEGER,
  "mid" INTEGER,
  "semester" VARCHAR(255),
  "years" VARCHAR(255),
  "capacity" INTEGER,
);

CREATE TABLE IF NOT EXISTS "room" (

);

CREATE TABLE IF NOT EXISTS "meeting" (

);