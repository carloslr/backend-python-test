"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
import sys
import subprocess
import os

from alayatodo import app, connect_db
from alayatodo.utils import hash_password

def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os.exit(1)


def _hash_passwords():
    try:
        db = connect_db()
        cur = db.execute("SELECT id, password FROM users")
        rs = cur.fetchall()
        for row in rs:
            (password, salt) = hash_password(row['password'])
            db.execute(
                "UPDATE users SET password = ?, password_salt = ? WHERE id = ?",
                (password, salt, row['id'])
            )
        db.commit()
        db.close()
    except Exception as ex:
        print(str(ex))
        os.exit(1)

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1 and args[1] == 'initdb':
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        _hash_passwords()
        print("AlayaTodo: Database initialized.")
    else:
        app.run(use_reloader=True)
