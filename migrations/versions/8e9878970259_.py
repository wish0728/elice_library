"""empty message

Revision ID: 8e9878970259
Revises: 
Create Date: 2021-11-27 22:43:56.544574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e9878970259'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Book',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=45), nullable=False),
    sa.Column('author', sa.String(length=45), nullable=True),
    sa.Column('publisher', sa.String(length=45), nullable=True),
    sa.Column('publication_date', sa.String(length=45), nullable=True),
    sa.Column('pages', sa.Integer(), nullable=True),
    sa.Column('isbn', sa.String(length=45), nullable=True),
    sa.Column('registered_date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('book_link', sa.String(length=255), nullable=True),
    sa.Column('book_status', sa.String(length=45), nullable=True),
    sa.Column('book_img', sa.String(length=45), nullable=True),
    sa.Column('at_user', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('User',
    sa.Column('email', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=True),
    sa.Column('phone', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('email'),
    sa.UniqueConstraint('email')
    )
    op.create_table('Review',
    sa.Column('review_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('user_id', sa.String(length=45), nullable=False),
    sa.Column('isbn', sa.String(length=45), nullable=True),
    sa.ForeignKeyConstraint(['isbn'], ['Book.isbn'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.email'], ),
    sa.PrimaryKeyConstraint('review_id')
    )
    op.create_table('checkoutRecords',
    sa.Column('checkout_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=45), nullable=True),
    sa.Column('checkoutdate', sa.Date(), nullable=True),
    sa.Column('duedate', sa.Date(), nullable=True),
    sa.Column('returndate', sa.Date(), nullable=True),
    sa.Column('isbn', sa.String(length=45), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['Book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.email'], ),
    sa.PrimaryKeyConstraint('checkout_id'),
    sa.UniqueConstraint('checkout_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('checkoutRecords')
    op.drop_table('Review')
    op.drop_table('User')
    op.drop_table('Book')
    # ### end Alembic commands ###
