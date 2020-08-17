DROP TABLE IF EXISTS "packages";
CREATE TABLE IF NOT EXISTS "packages"(
    "name" TEXT NOT NULL PRIMARY KEY,
    "version" TEXT,
    "descriptionSummary" TEXT,
    "description" TEXT
);

DROP TABLE IF EXISTS "dependencies";
CREATE TABLE IF NOT EXISTS "dependencies"(
    "id" INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    "dependent" TEXT,
    "dependency" TEXT,
    "substitutionId" TEXT,
    FOREIGN KEY("dependent") REFERENCES packages("id")
    -- Dependency can't be a foreign key, since there might be packages
    -- that are listed as dependencies, but can't be found in the file
);
