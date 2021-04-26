import sqlalchemy
from .db_session import SqlAlchemyBase
from datetime import date
from sqlalchemy import orm


class Game(SqlAlchemyBase):
    __tablename__ = 'games'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    designation = sqlalchemy.Column(sqlalchemy.String, unique=True)
    developer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    short_description_of_game = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    full_description_of_game = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    game_files = sqlalchemy.Column(sqlalchemy.String)
    game_upload_date = sqlalchemy.Column(sqlalchemy.Date, default=date.today())
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    icon = sqlalchemy.Column(sqlalchemy.String, default="/static/img/no_image.jpg")