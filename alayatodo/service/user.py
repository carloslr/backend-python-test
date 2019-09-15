from alayatodo.utils import verify_password
from alayatodo import get_db
from flask import (
    request
)

def login(username, password):
    sql = """
        SELECT
            id,
            username,
            password_salt,
            password,
            block_until > CURRENT_TIMESTAMP AS is_blocked,
            login_fail
        FROM users
        WHERE username = ?
        LIMIT 1
    """;
    cur = get_db().execute(sql, (username,))
    row = cur.fetchone()

    if row:
        user = {
            'id': row['id'],
            'username': row['username'],
            'ip': request.remote_addr
        }
        if row['is_blocked'] == 1:
            return (True, user)
        elif verify_password(row['password'], row['password_salt'], password):
            get_db().execute("""
                UPDATE users
                SET
                    login_count = login_count + 1,
                    login_fail = 0,
                    block_until = NULL,
                    last_login = CURRENT_TIMESTAMP
                WHERE
                    id = ?
            """, (row['id'],))
            get_db().commit()
            return (None, user)

        block_until = ''
        if row['login_fail'] + 1 >= MAX_ATTEMPT:
            block_until = f", block_until = datetime(CURRENT_TIMESTAMP, '+1 hours')"

        ok = get_db().execute(f"""
            UPDATE users
            SET
                login_fail = login_fail + 1
                {block_until}
            WHERE
                id = ?
        """, (row['id'],))
        get_db().commit()

        return (True, None)

    return (None, None)

