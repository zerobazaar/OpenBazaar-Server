import sqlite3
from config import DATA_FOLDER


def migrate(database_path):
    print "migrating to db version 2"
    conn = sqlite3.connect(database_path)
    conn.text_factory = str
    cursor = conn.cursor()

    # read hashmap from db
    cursor.execute('''SELECT * FROM hashmap''')
    mappings = cursor.fetchall()

    for mapping in mappings:
        if DATA_FOLDER not in mapping[1]:
            raise Exception("To complete migration 2 please run openbazaard at least once using the original "
                            "data folder location before moving it to a different location.")
        path = mapping[1][len(DATA_FOLDER):]
        cursor.execute('''INSERT OR REPLACE INTO hashmap(hash, filepath)
                          VALUES (?,?)''', (mapping[0], path))

    # update version
    cursor.execute('''PRAGMA user_version = 2''')
    conn.commit()
    conn.close()
