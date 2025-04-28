import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Planet(SqlAlchemyBase, UserMixin):

    __tablename__ = 'planets'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    star_system = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('star_systems.id'), nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)


