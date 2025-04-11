from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create tables based on the models
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(80), unique=True, nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, default='user'),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )

    op.create_table(
        'inventory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('item_name', sa.String(100), unique=True, nullable=False),
        sa.Column('total_stock', sa.Integer, nullable=False),
        sa.Column('unit_price', sa.Float, nullable=False),
        sa.Column('image_path', sa.String(255), nullable=True),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('subcategory', sa.String(100), nullable=True),
        sa.Column('product_code', sa.String(50), unique=True, nullable=True)
    )

    op.create_table(
        'sale',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('inventory.id'), nullable=False),
        sa.Column('quantity_sold', sa.Integer, nullable=False),
        sa.Column('total_price', sa.Float, nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False)
    )

    op.create_table(
        'stock_history',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('inventory.id'), nullable=False),
        sa.Column('quantity_changed', sa.Integer, nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False)
    )

def downgrade():
    # Drop tables in reverse order of creation
    op.drop_table('stock_history')
    op.drop_table('sale')
    op.drop_table('inventory')
    op.drop_table('user')