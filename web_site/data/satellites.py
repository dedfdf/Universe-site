import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Satellite(SqlAlchemyBase, UserMixin):

    __tablename__ = 'satellites'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    planet = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('planets.id'), nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)


