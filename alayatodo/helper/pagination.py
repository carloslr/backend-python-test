from math import ceil
from alayatodo import get_db

def query(sql, params, page, limit = 5):
    cur = get_db().execute(f"""
        SELECT COUNT(1) AS total
        FROM (
            {sql}
        )
    """, params)
    total = ceil(cur.fetchone()['total'] / limit)

    if page < 1:
        page = 1
    elif page > total:
        page = total

    rs = get_db().execute(f"""
        {sql}
        LIMIT {limit}
        OFFSET {(page - 1) * limit}
    """, params)
    pagination = {
        'total': total,
        'page': page,
    }
    return rs.fetchall(), pagination
