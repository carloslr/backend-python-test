from alayatodo import get_db
from flask import session

from alayatodo.helper.pagination import query

def get_by_id(id):
    cur = get_db().execute("""
        SELECT
            t.id,
            u.username,
            t.description,
            t.completed
        FROM todos t
        INNER JOIN users u
            ON u.id = t.user_id
        WHERE
            t.id = ?
            AND t.user_id = ?
    """, (id, session['user']['id']))
    return cur.fetchone()


def get_all(page = 1, limit = 5):
    return query("""
        SELECT
            t.id,
            u.username,
            t.description,
            t.completed
        FROM todos t
        INNER JOIN users u
            ON u.id = t.user_id
        WHERE t.user_id = ?
        ORDER BY t.completed, t.id
        """,
        (session['user']['id'], ),
        page,
        limit
    )
    pagination = {
        'total': 5,
        'page': page,
    }
    return cur.fetchall(), pagination


def create_todo(description):
    desc = description.strip()
    if desc != '' and len(desc) < 256:
        get_db().execute("""
            INSERT INTO todos (user_id, description, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (session['user']['id'], desc))
        get_db().commit()
        return True

    return False


def delete_todo(id):
    ok = get_db().execute("""
        DELETE FROM todos
        WHERE
            id = ?
            AND user_id = ?
    """, (id, session['user']['id']) )
    get_db().commit()
    return ok.rowcount > 0


def toggle_todo(id):
    get_db().execute("""
        UPDATE todos
        SET completed = 1 - (completed & 1)
        WHERE
            id = ?
            AND user_id = ?
    """, (id, session['user']['id']))
    get_db().commit()
