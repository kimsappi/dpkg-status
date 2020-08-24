DROP TABLE IF EXISTS "packages";
CREATE TABLE IF NOT EXISTS "packages"(
    "id" INTEGER PRIMARY KEY, -- SQLite does auto-incrementation automatically
    "name" TEXT NOT NULL,
    "version" TEXT,
    "descriptionSummary" TEXT,
    "description" TEXT
);

DROP TABLE IF EXISTS "dependencies";
CREATE TABLE IF NOT EXISTS "dependencies"(
    "id" INTEGER PRIMARY KEY,
    -- This is actually required, because a single package can be both a
    -- strict and substitutable dependency of another package
    -- (different versions, probably)
    "dependent" TEXT NOT NULL,
    "dependency" TEXT NOT NULL,
    -- Finding dependencies by string comparison feels really inefficient,
    -- but greatly simplifies the code as some packages are listed as
    -- dependencies despite not being found in dpkg/status
    "substitutionId" TEXT,
    FOREIGN KEY("dependent") REFERENCES packages("id")
    -- Dependency can't be a foreign key, since there might be packages
    -- that are listed as dependencies, but can't be found in the file
);

DROP VIEW IF EXISTS "dependentIdAndName";
CREATE VIEW IF NOT EXISTS "dependentIdAndName" AS
    SELECT p.id AS id, p."name" AS "name"
        FROM packages AS p
            INNER JOIN dependencies AS d ON d.dependent = p."name";

DROP VIEW IF EXISTS "dependencyIdAndNameAndSubId";
CREATE VIEW IF NOT EXISTS "dependencyIdAndNameAndSubId" AS
    SELECT DISTINCT p.id AS id, d.dependency AS "dependency",
            d.substitutionId AS substitutionId, d.dependent AS "dependent"
        FROM dependencies AS d
            LEFT OUTER JOIN packages AS p ON d.dependency = p."name";
