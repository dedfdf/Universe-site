import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Star_System(SqlAlchemyBase, UserMixin):

    __tablename__ = 'star_systems'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    galaxy = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('galaxies.id'), nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)


