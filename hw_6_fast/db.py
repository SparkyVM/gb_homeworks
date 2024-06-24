import databases
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from datetime import datetime

DATABASE_URL = "sqlite:///hw_6/mystore.db"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()


items = sa.Table(
    "items",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(30)),
    sa.Column("decription", sa.String(50)),
    sa.Column("price", sa.Float, nullable=False),
)

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(20)),
    sa.Column("last_name", sa.String(20)),
    sa.Column("email", sa.String(20), nullable=False),
    sa.Column("password", sa.String(8), nullable=False),
)

orders = sa.Table(
    "orders",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("id_user", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    sa.Column("id_item", sa.Integer, sa.ForeignKey('items.id'), nullable=False),
    sa.Column("created_at", sa.DateTime, default=datetime.now),
    sa.Column("status", sa.String(20)),

    sa.ForeignKeyConstraint(
        ["id_user"], ["users.id"], name="fk_parent_user_id",
    ),
    sa.ForeignKeyConstraint(
        ["id_item"], ["items.id"], name="fk_parent_item_id",
    ),
)

engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)