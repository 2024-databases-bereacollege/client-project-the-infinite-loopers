-- https://www.programiz.com/sql/insert-into

-- PRAGMA foreign_keys = ON;

-- CREATE TABLE IF NOT EXISTS "member"
-- (
--     memberId serial PRIMARY KEY NOT NULL,
--     firstName VARCHAR(100)  NOT NULL,
--     middleName VARCHAR(100),
--     lastName VARCHAR(100),
--     phoneNumber VARCHAR(15),
--     score INTEGER NOT NULL,
--     memberAddress VARCHAR NOT NULL,
--     NumberOfEventsAttended INTEGER NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS "chapter"
-- (
--     chapterName VARCHAR PRIMARY KEY NOT NULL,
--     memberId INTEGER,
--     numberofMembers INTEGER  NOT NULL,
--     chapterLead VARCHAR(100),
--     chapterEmail VARCHAR(50),
--     FOREIGN KEY (memberId) REFERENCES member(memberId)
-- 		ON DELETE NO ACTION 
--         ON UPDATE NO ACTION
-- );

-- CREATE TABLE IF NOT EXISTS "event"
-- (
--     eventName VARCHAR PRIMARY KEY NOT NULL,
--     venue VARCHAR(100)  NOT NULL,
--     theme VARCHAR(100) NOT NULL,
--     eventDate DATETIME,
--     numberofMemebersAttended INTEGER
-- );

-- CREATE TABLE IF NOT EXISTS "donation"
-- (
--     donationId serial PRIMARY KEY  NOT NULL,
--     monetaryWorth INTEGER  NOT NULL,
--     item VARCHAR  NOT NULL
-- );

INSERT INTO member (Score, phoneNumber, firstName, middleName, lastName, memberAddress, NumberOfEventsAttended, status)
VALUES
    (987, 1234567890, 'Betty', 'M', 'Hibler', '314 Prospect St, Berea, KY, 40403',  5, 'active'),
    (654, 2345678901, 'Landra', '', 'Lewis', '619 Chestnut St, Berea, KY, 40403', 3, 'active'),
    (321, 3456789012, 'Travis', '', 'Bolinger', '314 University Dr Apt A, Richmond, KY, 2841',  2, 'active'),
    (432, 4567890123, 'Rachel', '',  'White', '1101 Elm St, Danville, KY, 40422', 7, 'active'),
    (876, 5678901234, 'Joanie', '', 'Lukins', '503 Ohara Dr, Daville, KY, 40422', 4, 'active');   

INSERT INTO chapter (chapterName, numberofMembers, chapterLead, chapterEmail)
VALUES
    ('Madison County', 50, 'Landra Lewis', 'alex@example.com'),
    ('Wilderness Trace', 30, 'Emily Brown', 'emily@example.com');


INSERT INTO donation (donor_id, item, "monetaryWorth")
VALUES
    (1, 'Laptop', 800),
    (2, 'Books', 100),
    (3, 'Laptop', 800),
    (2, 'Books', 100),
    (1, 'Laptop', 800);

INSERT INTO event (eventName, venue, theme, eventDate, numberofMembersAttended)
VALUES
    ('Community Building', 'Convention Center', 'Environmental Preservation', '2024-04-01', 200),
    ('Workshop', 'Community Center', 'Environmental Preservation', '2024-04-15', 80),
    ('Hackathon', 'Convention Center', 'Environmental Preservation', '2024-04-01', 200),
    ('Seedy Workshop', 'Community Center', 'Environmental Preservation', '2024-04-15', 80),
    ('How to sleep in class', 'Community Center', 'Sleep', '2024-04-15', 80);