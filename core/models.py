from copy import deepcopy
from typing import Any, TypeVar, Type, Dict, Optional, cast, List

from dateutil import parser
from sqlalchemy.orm.session import make_transient

from core.main import db
from core.settings import Config

T = TypeVar('T', bound='Model')


class Model(db.Model):  # type:ignore
    __abstract__ = True
    __table_args__ = Config.DATABASE_SCHEMA

    @classmethod
    def find(cls: Type[T], id: Dict[str, Any]) -> Optional[T]:
        return cast(Optional[T], cls.query.filter_by(**id).first())

    @classmethod
    def create(cls: Type[T], **kwargs: Dict[str, Any]) -> T:
        instance = None
        try:
            instance = cls.validate(cls(**kwargs))
            db.session.add(instance)
            # instance = deepcopy(instance)
            db.session.commit()
        except Exception as e:  # TODO: Create custom exception
            db.session.rollback()
            raise e

        return instance

    def create_clone(self, **kwargs: Dict[str, Any]) -> T:
        try:
            db.session.expunge(self)
            make_transient(self)
            for key in kwargs:
                setattr(self, key, kwargs[key])
            self = self.validate(self)
            db.session.add(self)
            print(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs: Dict[str, Any]) -> T:
        try:
            for key in kwargs:
                setattr(self, key, kwargs[key])
            self = self.validate(self)
            db.session.commit()
            return self
        except Exception as e:  # TODO: Create custom exception
            db.session.rollback()
            raise e

    def get(self, att:str) -> Any:
        return getattr(self, att, '')

    @classmethod
    def delete(cls: Type[T], **kwargs: Dict[str, Any]) -> bool:
        try:
            instance = cls.validate(cls(**kwargs))
            db.session.delete(instance)
            instance = deepcopy(instance)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return True

    @classmethod
    def validate(cls: Type[T], instance: T) -> T:
        model_columns = cls.__table__.columns

        # Get all date and datetime column names
        datetime_columns = filter(lambda column: isinstance(
            column.type, (db.Date, db.DateTime, db.TIMESTAMP)), model_columns)
        # Parse all date and datetime strings to python datetime instances
        for column in datetime_columns:
            value = getattr(instance, column.name)
            if value and isinstance(value, str):
                setattr(instance, column.name, parser.parse(value))

        return instance
