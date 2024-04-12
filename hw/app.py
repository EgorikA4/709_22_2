"""Flask homework."""
import os

import const
import db_query
import flask
import http_codes
from db import connect
from psycopg2.errors import InvalidTextRepresentation
from psycopg2.sql import SQL, Identifier, Literal

app = flask.Flask(__name__)
app.json_ensure_ascii = False

connection = connect()
connection.autocommit = True

DEFAULT_FLASK_PORT = 5000


@app.get('/')
def main_page() -> tuple[str, int]:
    """Display the main page of the site.

    Returns:
        welcome message and status code OK.
    """
    return '<p>Hello, World!</p>', http_codes.OK


@app.get('/properties')
def get_properties() -> tuple[str, int]:
    """Read properties.

    Returns:
        properties with their owners and hcs.
    """
    with connection.cursor() as cursor:
        cursor.execute(db_query.GET_PROPERTIES)
        return cursor.fetchall(), http_codes.OK


def _check_positive_numbers(*nums) -> bool:
    for num in nums:
        if not isinstance(num, int | float):
            return False
        elif num < 0:
            return False
    return True


def _check_properties_kwargs(kwargs: dict) -> bool:
    id_ = kwargs.get(const.PROPS_ID, None)
    if id_ and not _get_entity_id(id_, const.PROPS_TABLE_NAME):
        return False

    for column in (const.PROPS_ADDRESS, const.PROPS_PRICE, const.PROPS_SQUARE):
        if column not in kwargs:
            return False

        elif column in {const.PROPS_SQUARE, const.PROPS_PRICE}:
            try:
                kwargs[column] = float(kwargs[column])
            except ValueError:
                return False

    return _check_positive_numbers(
        kwargs[const.PROPS_SQUARE],
        kwargs[const.PROPS_PRICE],
    )


def _get_entity_id(id_: str, table_name: str) -> str | None:
    with connection.cursor() as cursor:
        query = SQL(db_query.GET_ENTITY).format(
            table=Identifier(table_name),
            id_=Literal(id_),
        )
        try:
            cursor.execute(query)
        except InvalidTextRepresentation:
            return False
        return id_ if bool(cursor.fetchone()) else None


@app.post('/properties/create')
def create_properties() -> tuple[str, int]:
    """Create properties record in db.

    Returns:
        id of the created record.
    """
    body = flask.request.json

    if not _check_properties_kwargs(body):
        return '', http_codes.BAD_REQUEST

    hcs_id = _get_entity_id(
        body.get(const.PROPS_HCS_ID, None),
        const.HCS_TABLE_NAME,
    )

    query = SQL(db_query.CREATE_PROPERTIES).format(
        address=Literal(body[const.PROPS_ADDRESS]),
        square=Literal(body[const.PROPS_SQUARE]),
        price=Literal(body[const.PROPS_PRICE]),
        hcs_id=Literal(hcs_id),
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone(), http_codes.CREATED


def _get_hcs_id(id_: str) -> str | None:
    with connection.cursor() as cursor:
        query = SQL(db_query.GET_HCS_ID).format(id_=Literal(id_))
        cursor.execute(query)
        return cursor.fetchone()[const.PROPS_HCS_ID]


@app.post('/properties/update')
def update_properties() -> tuple[str, int]:
    """Update properties record in db.

    Returns:
        id of the updated record.
    """
    body = flask.request.json

    id_ = body.get(const.PROPS_ID, None)
    if not _check_properties_kwargs(body):
        return '', http_codes.BAD_REQUEST

    hcs_id = body.get(const.PROPS_HCS_ID, None)
    if not hcs_id or not _get_entity_id(hcs_id, const.PROPS_TABLE_NAME):
        hcs_id = _get_hcs_id(id_)

    query = SQL(db_query.UPDATE_PROPERTIES).format(
        id_=Literal(id_),
        address=Literal(body[const.PROPS_ADDRESS]),
        square=Literal(body[const.PROPS_SQUARE]),
        price=Literal(body[const.PROPS_PRICE]),
        hcs_id=Literal(hcs_id),
    )

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone(), http_codes.NO_CONTENT


@app.post('/properties/delete')
def delete_properties():
    """Delete properties record from db.

    Returns:
        status code 'no content'.
    """
    body = flask.request.json

    id_ = body.get(const.PROPS_ID, None)

    if not _get_entity_id(id_, const.PROPS_TABLE_NAME):
        return '', http_codes.BAD_REQUEST

    remove_properties_links = SQL(db_query.DELETE_PROPERTIES_LINKS).format(
        id_=Literal(id_),
    )
    remove_properties = SQL(db_query.DELETE_PROPERTIES).format(
        id_=Literal(id_),
    )
    with connection.cursor() as cursor:
        cursor.execute(remove_properties_links)
        cursor.execute(remove_properties)
        return '', http_codes.NO_CONTENT


if __name__ == '__main__':
    try:
        port = int(os.getenv('FLASK_PORT', DEFAULT_FLASK_PORT))
    except ValueError:
        port = DEFAULT_FLASK_PORT
    app.run(port=DEFAULT_FLASK_PORT)
