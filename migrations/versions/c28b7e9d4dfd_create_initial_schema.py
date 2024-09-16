"""Create initial schema

Revision ID: c28b7e9d4dfd
Revises: 
Create Date: 2024-09-15 14:30:00
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'c28b7e9d4dfd'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create bands table
    op.create_table(
        'band',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('hometown', sa.String, nullable=False),
    )

    # Create venues table
    op.create_table(
        'venue',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('city', sa.String, nullable=False),
    )

    # Create concerts table
    op.create_table(
        'concert',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('band_id', sa.Integer, sa.ForeignKey('band.id'), nullable=False),
        sa.Column('venue_id', sa.Integer, sa.ForeignKey('venue.id'), nullable=False),
        sa.Column('date', sa.String, nullable=False),
    )

    # Create association table for many-to-many relationship
    op.create_table(
        'band_venue',
        sa.Column('band_id', sa.Integer, sa.ForeignKey('band.id'), primary_key=True),
        sa.Column('venue_id', sa.Integer, sa.ForeignKey('venue.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('band_venue')
    op.drop_table('concert')
    op.drop_table('venue')
    op.drop_table('band')
