#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class UserTable:

    NAME = "user"

    SCHEMA = """
        CREATE TABLE user (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            forename    TEXT NOT NULL,
            surname    TEXT NOT NULL,
            username    TEXT NOT NULL,
            pass_hash    TEXT NOT NULL,
            is_admin        INTEGER DEFAULT 0
        )
    """

    SEED_DATA = """
        INSERT INTO user (forename, surname, username, pass_hash)
VALUES ("john", "seed data", "johnSeedData", "scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252" ),
       ("micheal", "is better than helen", "iMissMicheal", "scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252" ),
("hantu", "itgottabeahantu", "itsafrickenmimic", "scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252" )
    """

class MessagesTable:

    NAME = "message"

    SCHEMA = """
        CREATE TABLE message (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            title   TEXT NOT NULL,
            body    TEXT NOT NULL,

             FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """

    SEED_DATA = """
        INSERT INTO message (user_id, title, body) VALUES 
(1, 'Im a test message!!!!', 'PLEASE LET ME OUT'), 
(2, 'i miss micheal the micheal monster', 'AHHHHHHHHHHHHHHHH'), 
(3, 'i love phasmophobia until its a mimic', 'i hatew mimics');

"""

# Add more table classes here...



#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1,
#     Table2,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
#       foreign keys AFTER the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    UserTable,
    MessagesTable
    # Add more tables here...
]

