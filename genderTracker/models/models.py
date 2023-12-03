from genderTracker.setup import db
import uuid
from sqlalchemy.dialects.postgresql import TEXT, ARRAY, JSON, UUID
from sqlalchemy.sql import func
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    display_name = db.Column(TEXT)
    ui_settings = db.Column(JSON)
    password = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    last_login = db.Column(db.DateTime(timezone=True), default=func.now())
    last_ip = db.Column(db.String(100))
    last_user_agent = db.Column(db.String(1000))
    last_country = db.Column(db.String(1000))
    last_city = db.Column(db.String(1000))
    last_timezone = db.Column(db.String(1000))
    num_logins = db.Column(db.Integer, default=0)
    enabled = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    salt = db.Column(db.String(100), nullable=False)

    keys = db.relationship('Key', backref='user', lazy=True)

    def __init__(self, username, email, password, ip=None, user_agent=None, country=None, city=None, timezone=None, admin=False, enabled=True):
        self.update_username(username)
        self.email = email
        self.password, self.salt = self.hash_plain_password(password)
        self.last_ip = ip
        self.last_user_agent = user_agent
        self.last_country = country
        self.last_city = city
        self.last_timezone = timezone
        self.admin = admin
        self.enabled = enabled

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'username': self.username,
            'display_name': self.display_name,
            'ui_settings': self.ui_settings,
            'email': self.email,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'last_ip': self.last_ip,
            'last_user_agent': self.last_user_agent,
            'last_country': self.last_country,
            'last_city': self.last_city,
            'last_timezone': self.last_timezone,
            'num_logins': self.num_logins,
            'num_queries': self.num_queries,
            'can_query': self.can_query,
            'enabled': self.enabled,
            'admin': self.admin
        }

    def hash_plain_password(self, plain_password, salt=None):
        if not salt:
            salt = bcrypt.gensalt().decode('utf-8')
        hashedPass = bcrypt.hashpw(plain_password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        return hashedPass, salt

    def check_password(self, plain_password):
        return self.hash_plain_password(plain_password, salt=self.salt)[0] == self.password

    def update_password(self, plain_password, new_password):
        if self.check_password(plain_password):
            self.password, self.salt = self.hash_plain_password(new_password)
            return True
        return False

    def update_last_login(self, ip, user_agent, country, city, timezone):
        self.last_login = func.now()
        self.last_ip = ip
        self.last_user_agent = user_agent
        self.last_country = country
        self.last_city = city
        self.last_timezone = timezone
        self.num_logins += 1

    def update_username(self, new_username):
        # Check if any other users have the same username
        checkUser = User.query.filter_by(username=new_username).first()
        if checkUser:
            return False
        self.username = new_username
        return True

    def update_display_name(self, new_display_name):
        self.display_name = new_display_name
        return True

    def update_email(self, new_email):
        self.email = new_email
        return True

    def update_enabled(self, new_enabled):
        self.enabled = new_enabled
        return True

    def disable(self):
        return self.update_enabled(False)

    def __repr__(self):
        return f'<User: {self.username}>'


class Gender(db.Model):
    __tablename__ = "genders"
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(TEXT, unique=True, nullable=False)
    pronouns = db.Column(ARRAY(TEXT), nullable=True)
    description = db.Column(TEXT, nullable=True)


    def __init__(self, name, pronouns, description):
        self.name = name
        self.pronouns = pronouns
        self.description = description

    def __repr__(self):
        return f"<Gender: {self.name} ({'/'.join(self.pronouns)})>"

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "pronouns": self.pronouns,
            "description": self.description
        }



class Day(db.Model):
    __tablename__ = "days"
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False, primary_key=False)
    gender_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('genders.uuid'), nullable=False, primary_key=False)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    description = db.Column(TEXT, nullable=True)
    name = db.Column(TEXT, nullable=True, default=None)

    def __init__(self, user_uuid, gender_uuid, description=None):
        self.user_uuid = user_uuid
        self.gender_uuid = gender_uuid
        self.description = description

    def __repr__(self):
        return f"<Day: {self.datetime} ({self.user_uuid})>"

    def to_dict(self):
        return {
            "user_uuid": self.user_uuid,
            "datetime": self.datetime,
            "gender_uuid": self.gender_uuid,
            "description": self.description,
            }

class Key(db.Model):
    __tablename__ = "keys"
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = db.Column(db.String(32), nullable=False)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    last_used = db.Column(db.DateTime(timezone=True))
    uses = db.Column(db.Integer, default=0)
    salt = db.Column(db.String(100), nullable=False)
    max_uses = db.Column(db.Integer, default=2147483647)

    def __init__(self, user_uuid, key, max_uses=2147483647):
        self.user_uuid = user_uuid
        self.max_uses = max_uses
        self.key, self.salt = self._hash_key(key)

    @staticmethod
    def _hash_key(key, salt=None):
        print(key, salt)
        if salt is None:
            salt = bcrypt.gensalt().decode('utf-8')
        hashedKey = bcrypt.hashpw(key.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        return hashedKey, salt

    def check_key(self, key):
        return self._hash_key(key, salt=self.salt)[0] == self.key


    def __repr__(self):
        return f'<Key: {self.key}, user: {self.user_uuid}>'
