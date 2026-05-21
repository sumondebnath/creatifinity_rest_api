from django.db import migrations, connection


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_user_alter_review_user'),
    ]

    def run_if_postgres(apps, schema_editor):
        """Only run PostgreSQL-specific operations"""
        if schema_editor.connection.vendor != 'postgresql':
            return
        
        cursor = schema_editor.connection.cursor()
        
        # Drop legacy account_id column if it exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.COLUMNS 
                WHERE table_name='blog_blog' AND column_name='account_id'
            );
        """)
        if cursor.fetchone()[0]:
            cursor.execute("ALTER TABLE blog_blog DROP COLUMN account_id;")
        
        # Make image nullable
        cursor.execute("""
            ALTER TABLE blog_blog ALTER COLUMN image DROP NOT NULL;
        """)
        
        # Change rating from varchar to integer
        cursor.execute("""
            ALTER TABLE blog_review ALTER COLUMN rating TYPE integer 
            USING rating::integer;
        """)
        
        # Make review.user_id nullable
        cursor.execute("""
            ALTER TABLE blog_review ALTER COLUMN user_id DROP NOT NULL;
        """)
        
        # Change review.user_id to bigint
        cursor.execute("""
            ALTER TABLE blog_review ALTER COLUMN user_id TYPE bigint 
            USING user_id::bigint;
        """)
        
        # Add unique constraint if it doesn't exist
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conrelid = 'blog_review'::regclass
                      AND contype = 'u'
                      AND conname LIKE 'blog_review_user_id_blog_id%'
                ) THEN
                    ALTER TABLE blog_review
                        ADD CONSTRAINT blog_review_user_id_blog_id_uniq
                        UNIQUE (user_id, blog_id);
                END IF;
            END $$;
        """)

    def reverse_if_postgres(apps, schema_editor):
        """Reverse operations only for PostgreSQL"""
        if schema_editor.connection.vendor != 'postgresql':
            return
        
        cursor = schema_editor.connection.cursor()
        cursor.execute("""
            ALTER TABLE blog_review DROP CONSTRAINT IF EXISTS 
            blog_review_user_id_blog_id_uniq;
        """)

    operations = [
        migrations.RunPython(run_if_postgres, reverse_if_postgres),
    ]
