CREATE TABLE episode (
	episode INT NOT NULL, 
	season INT NOT NULL, 
	episode_in_season INT NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	air_date DATETIME NOT NULL, 
	opening_line VARCHAR(255) NOT NULL, 
	PRIMARY KEY (episode)
);
CREATE TABLE director (
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (name)
);
CREATE TABLE writer (
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (name)
);
CREATE TABLE replik (
	 id INT NOT NULL, 
    season INT NOT NULL, 
    episode INT, 
    `character` VARCHAR(255) NOT NULL, 
    line TEXT NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY (episode) REFERENCES episode (episode)
);
CREATE TABLE episodedirector (
	episode INT NOT NULL, 
	director VARCHAR(255) NOT NULL, 
	PRIMARY KEY (episode, director), 
	FOREIGN KEY(episode) REFERENCES episode (episode), 
	FOREIGN KEY(director) REFERENCES director (name)
);
CREATE TABLE episodewriter (
	episode INT NOT NULL, 
	writer VARCHAR(255) NOT NULL, 
	PRIMARY KEY (episode, writer), 
	FOREIGN KEY(episode) REFERENCES episode (episode), 
	FOREIGN KEY(writer) REFERENCES writer (name)
);
