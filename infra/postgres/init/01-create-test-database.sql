-- Runs once, when the postgres volume is first created.
-- The test suite uses a separate database so a test run can never touch development data.
CREATE DATABASE atlas_test OWNER atlas;
