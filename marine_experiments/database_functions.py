"""Functions that interact with the database."""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(dbname,
                      password="postgres") -> connection:
    """Returns a DB connection."""

    return connect(dbname=dbname,
                   host="localhost",
                   port=5432,
                   password=password,
                   cursor_factory=RealDictCursor)


def get_experiment(conn, exp_type=None, score_over=None):

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
    SELECT
        e.experiment_id,
        e.subject_id,
        sp.species_name AS species,
        TO_CHAR(e.experiment_date, 'YYYY-MM-DD') AS experiment_date,
        et.type_name AS experiment_type,
        CONCAT(
            ROUND((e.score::numeric / et.max_score) * 100, 2),
            '%'
        ) AS score
    FROM experiment e
    JOIN experiment_type et
        ON e.experiment_type_id = et.experiment_type_id
    JOIN subject s
        ON e.subject_id = s.subject_id
    JOIN species sp
        ON s.species_id = sp.species_id
    """

    conditions = []
    params = {}

    if exp_type:
        conditions.append("LOWER(et.type_name) = %(type)s")
        params["type"] = exp_type.lower()

    if score_over is not None:
        conditions.append(
            "((e.score::numeric / et.max_score) * 100) >= %(score_over)s")
        params["score_over"] = score_over

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
    ORDER BY
        e.experiment_date DESC,
        et.type_name ASC,
        e.subject_id ASC,
        e.experiment_id ASC
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()

    return rows


def get_experiment_by_id(conn: connection, experiment_id: int) -> dict:
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            experiment_id,
            TO_CHAR(experiment_date, 'YYYY-MM-DD') AS experiment_date
        FROM experiment
        WHERE experiment_id = %(experiment_id)s
    """, {"experiment_id": experiment_id})

    row = cursor.fetchone()

    cursor.close()

    return row

    ...


def delete_experiment(conn: connection, experiment_id: int) -> dict:
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    experiment = get_experiment_by_id(conn, experiment_id)

    if not experiment:
        cursor.close()
        return None

    cursor.execute(
        """
    DELETE FROM experiment
    WHERE experiment_id = %(experiment_id)s
    """,
        {"experiment_id": experiment_id}
    )
    conn.commit()

    cursor.close()

    return experiment
