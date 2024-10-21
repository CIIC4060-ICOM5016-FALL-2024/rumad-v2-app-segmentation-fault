-- COURSES TABLE
CREATE TABLE IF NOT EXISTS "class" (
  "cid" SERIAL PRIMARY KEY,
  "cname" VARCHAR(50),
  "ccode" VARCHAR(4),
  "cdesc" VARCHAR(100),
  "term" VARCHAR(35),
  "years" VARCHAR(20),
  "cred" INTEGER NOT NULL,
  "csyllabus" VARCHAR(255)
);

-- ROOM TABLE
CREATE TABLE IF NOT EXISTS "room" (
    "rid" SERIAL PRIMARY KEY,
    "building" VARCHAR(10),
    "room_number" VARCHAR,
    "capacity" INTEGER
);

-- MEETING TABLE
CREATE TABLE IF NOT EXISTS "meeting" (
    "mid" SERIAL PRIMARY KEY,
    "ccode" VARCHAR(4),
    "starttime" TIME,
    "endtime" TIME,
    "cdays" VARCHAR(5) 
);

-- SECTION TABLE
CREATE TABLE IF NOT EXISTS "section" (
  "sid" SERIAL PRIMARY KEY,
  "roomid" INTEGER,
  "cid" INTEGER,
  "mid" INTEGER,
  "semester" VARCHAR(10),
  "years" VARCHAR(4),
  "capacity" INTEGER,

  FOREIGN KEY ("roomid") REFERENCES "room"("rid"),
  FOREIGN KEY ("cid") REFERENCES "class"("cid"),
  FOREIGN KEY ("mid") REFERENCES "meeting"("mid")
);

-- VECTOR EXTENSION
CREATE EXTENSION IF NOT EXISTS vector;

-- SYLLABUS TABLE
CREATE TABLE IF NOT EXISTS "syllabus" (
  "chunkid" SERIAL PRIMARY KEY,
  "courseid" INTEGER,
  "embedding_text" vector(500),
  "chunk" VARCHAR(255),

  FOREIGN KEY ("courseid") REFERENCES "class"("cid")
);

-- REQUISITE TABLE
CREATE TABLE IF NOT EXISTS "requisite" (
  "classid" INTEGER,
  "reqid" INTEGER,
  "prereq" BOOLEAN,

  PRIMARY KEY ("classid", "reqid"),
  FOREIGN KEY ("classid") REFERENCES "class"("cid"),
  FOREIGN KEY ("reqid") REFERENCES "class"("cid")
);






