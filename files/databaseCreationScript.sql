--
-- Use this script to create your database
--
-- 1. Connect to your remote instance of MySQL via MySQLShell
--    \c cbcradio_bds99@cbcradio.org
-- 2. At the mysql> prompt, navigate to your database
--    use cbcradio_bds754_99
-- 3. Use the source command to execute this SQL script
--    If your script is saved in the C:\temp folder
--    > source C:\temp\databaseCreationScript.sql
--

-- NOTE: Change this to YOUR database
USE cbcradio_bds754_7;

-- This will delete the table if it exists.
DROP TABLE IF EXISTS `housing`;

CREATE TABLE housing
               (
                `id`                 int not null auto_increment primary key,
                `guid`               char(36) not null,
                `zip_code`           int not null,
                `city`               char(32) not null,
                `state`              char(2) not null,
                `county`             char(32) not null,
                `median_age`         int not null,
                `total_rooms`        int not null,
                `total_bedrooms`     int not null,
                `population`         int not null,
                `households`         int not null,
                `median_income`      int not null,
                `median_house_value` int not null
               );

-- Now, you can use the desc command to see that the table has been added.
--
-- > desc housing;
-- +--------------------+----------+------+-----+---------+----------------+
-- | Field              | Type     | Null | Key | Default | Extra          |
-- +--------------------+----------+------+-----+---------+----------------+
-- | id                 | int(11)  | NO   | PRI | NULL    | auto_increment |
-- | guid               | char(36) | NO   |     | NULL    |                |
-- | zip_code           | int(11)  | NO   |     | NULL    |                |
-- | city               | char(32) | NO   |     | NULL    |                |
-- | state              | char(2)  | NO   |     | NULL    |                |
-- | county             | char(32) | NO   |     | NULL    |                |
-- | median_age         | int(11)  | NO   |     | NULL    |                |
-- | total_rooms        | int(11)  | NO   |     | NULL    |                |
-- | total_bedrooms     | int(11)  | NO   |     | NULL    |                |
-- | population         | int(11)  | NO   |     | NULL    |                |
-- | households         | int(11)  | NO   |     | NULL    |                |
-- | median_income      | int(11)  | NO   |     | NULL    |                |
-- | median_house_value | int(11)  | NO   |     | NULL    |                |
-- +--------------------+----------+------+-----+---------+----------------+