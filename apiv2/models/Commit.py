import apiv2.models.User as User
from apiv2 import db
from . import Utils
import datetime


class Commit(db.Model):
    """
    Commit dataclass, has:
    - Creator
    - Time
    - Lines added
    - Lines removed
    - uuid
    - comment (max 256 chars)
    """
    __tablename__ = "commits"
    _id = db.Column(db.Integer, primary_key=True, name='id')
    _user_ID = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    uuid = db.Column(db.String(40), nullable=False, default=Utils.str_uuid4)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    # Relationships
    creator = db.relationship("User", backref=db.backref("commits", cascade="all,delete"), lazy="joined")

    @db.validates("uuid")
    def uuid_edit_block(self, key, value):
        """This will prevent you from changing the UUID of this object when editing"""
        if self.uuid:  # Already exists
            raise ValueError("UUID is autogenerated and can not be modified!")
        return value

    def __init__(self,
                 creator: User.User,
                 description: str | None = None,
                 date: datetime.datetime | None = None):
        self.creator = creator
        self.description = description
        if date:
            self.date = date

    def __repr__(self):
        return f"[COMMIT] {self.creator.nick}: {self.description}"
