
BEGIN TRANSACTION;


-- Club Members --

CREATE TABLE ClubMembers (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	fName TEXT NOT NULL,
	sName TEXT NOT NULL,
	birthdate TEXT NULL
);

INSERT INTO ClubMembers (fName, sName, birthdate) VALUES
('John', 'Smith', '1972-06-11'),
('Benjamin', 'Woods', '1984-10-02'),
('Skye', 'Jones', '1986-01-24'),
('Jessica', 'Tayler', '1967-12-31'),
('Linda', 'Smith', '1991-05-13'),
('Gary', 'Johnston', '1994-04-28'),
('Joseph', 'Little', '2001-07-31'),
('Larry', 'Henderson', '1999-04-17'),
('Patricia', 'Nielson', '1997-02-14'),
('Christopher', 'Edwards', '1989-11-03')
;

END TRANSACTION;
