
BEGIN TRANSACTION;

CREATE TABLE Topic (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT NOT NULL,
	lesson BLOB NOT NULL,
	video TEXT DEFAULT NULL
);

 CREATE TABLE Question (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	description BLOB NOT NULL,
	resultQuery TEXT NOT NULL,
	dataViewQuery TEXT NOT NULL,
	topicId INTEGER NOT NULL,
	title TEXT NOT NULL,
	FOREIGN KEY(topicId) REFERENCES Topic(id)
);

INSERT INTO Topic (name, lesson, video) VALUES 
(
'SELECT'
,
'<h1><b>Using SELECT to , erm... SELECT</b></h1>'
,
NULL
)
,
(
'WHERE'
,
'<h1><b>WHERE is the thing I am looking for?</h1><b>'
,
NULL
)
;


INSERT INTO Question (description, resultQuery, dataViewQuery, topicId, title) VALUES

-- Questions for Topic 'SELECT' 
(
'<h1>First Names</h1>
From the table ClubMembers<br>
list the first name of every member<br>
<br>
Table ClubMembers<br>
fName, sName, birthdate'
,
'SELECT fName AS ''First Name'' FROM ClubMembers'
,
'SELECT * FROM ClubMembers'
,
(SELECT id FROM Topic WHERE name = 'SELECT')
,
'List First Names'
)
,
(
'<h1>Surnames</h1>
From the table ClubMembers<br>
list the surname of every member<br>
<br>
Table ClubMembers<br>
fName, sName, birthdate'
,
'SELECT sName AS Surname FROM ClubMembers'
,
'SELECT * FROM ClubMembers'
,
(SELECT id FROM Topic WHERE name = 'SELECT')
,
'List Surnames'
)
,

-- Questions for Topic 'WHERE'
(
'<h1>Memeber details</h1>
From the table ClubMembers<br>
List the First Name, Surname and Birthdate<br>
of the member John Smith
<br>
Table ClubMembers<br>
fName, sName, birthdate'
,
'SELECT fName AS ''First Name'', sName AS Surname, birthdate AS Birthdate 
FROM ClubMembers 
WHERE fName = ''John'' 
AND sName = ''Smith'''
,
'SELECT * FROM ClubMembers'
,
(SELECT id FROM Topic WHERE name = 'WHERE')
,
'List Member Details'
);


COMMIT;
