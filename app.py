import os

import psycopg2
from flask import Flask, request
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Literal

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False

connection = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST") if os.getenv("DEBUG_MODE") == "false" else "localhost",
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    cursor_factory=RealDictCursor
)
connection.autocommit = True


def check_limits(number: float | int) -> bool:
    return True if number < 0 or number > 5 else False


@app.get("/")
def hello_world():
    return "<p>CRUD app on flask about theaters and performances</p>"


@app.get("/theaters")
def get_theaters():
    query = """
    with theaters_with_performances as (
        select
            t.id,
            t.title,
            t.address,
            t.rating,
            coalesce(json_agg(json_build_object(
                'id', p.id, 'title', p.title, 'description', p.description, 'date', p.date))
                    filter (where p.id is not null), '[]') as performances
        from theaters.theater t
        left join theaters.theater_performance tp on t.id = tp.theater_id
        left join theaters.performance p on p.id = tp.performance_id
        group by t.id
    ),
    theaters_with_tickets as (
        select
            tr.id,
            coalesce(json_agg(json_build_object(
                'id', tt.id, 'time', tt.time, 'place', tt.place))
                    filter (where tt.id is not null), '[]') as tickets
        from theaters.theater tr
        left join theaters.theater_performance tp on tr.id = tp.theater_id
        left join theaters.ticket tt on tp.id = tt.theater_performance_id
        group by tr.id
    )
    select twp.id, title, address, rating, performances, tickets
    from theaters_with_performances twp
    join theaters_with_tickets twt on twp.id = twt.id
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result


@app.post("/theaters/create")
def create_theater():
    body = request.json

    title = body["title"]
    address = body["address"]
    rating = body["rating"]

    if check_limits(rating):
        return "Rating must be between 0 and 5", 400

    query = SQL("""
    insert into theaters.theater(title, address, rating) values
    ({title}, {address}, {rating})
    returning id
    """).format(title=Literal(title), address=Literal(address), rating=Literal(rating))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return result, 201


@app.put("/theaters/update")
def update_theater():
    body = request.json

    id = body["id"]
    title = body["title"]
    address = body["address"]
    rating = body["rating"]

    if check_limits(rating):
        return "Rating must be between 0 and 5", 400

    query = SQL("""
    update theaters.theater
    set
        title = {title},
        address = {address},
        rating = {rating}
    where id = {id}
    returning id
    """).format(title=Literal(title), address=Literal(address), rating=Literal(rating), id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    if len(result) == 0:
        return 'Theater not found', 404

    return result


@app.delete("/theaters/delete")
def delete_theater():
    body = request.json

    id = body["id"]

    del_theater_link = SQL("""
    delete from theaters.theater_performance where theater_id = {id}
    """).format(id=Literal(id))

    del_theater = SQL("""
    delete from theaters.theater where id = {id}
    returning id
    """).format(id=Literal(id))

    with connection.cursor() as cursor:
        cursor.execute(del_theater_link)
        cursor.execute(del_theater)
        result = cursor.fetchall()

    if len(result) == 0:
        return "Theater not found", 404

    return "", 204


if __name__ == "__main__":
    app.run(port=os.getenv("FLASK_PORT"))
