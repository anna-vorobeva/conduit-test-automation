import psycopg
from psycopg.rows import dict_row


class ConduitDb:
    """Read-only access to the Conduit database, to verify what the API actually persisted."""

    def __init__(self, dsn: str) -> None:
        self._conn = psycopg.connect(dsn, row_factory=dict_row, autocommit=True)

    def close(self) -> None:
        self._conn.close()

    def find_user(self, email: str) -> dict | None:
        return self._fetch_one(
            "SELECT username, email, password FROM accounts_user WHERE email = %s", (email,)
        )

    def find_article(self, slug: str) -> dict | None:
        return self._fetch_one(
            "SELECT slug, title, summary, content FROM articles_article WHERE slug = %s", (slug,)
        )

    def _fetch_one(self, query: str, params: tuple) -> dict | None:
        with self._conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()
