from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_user_alter_review_user'),
    ]

    operations = [
        # Drop legacy account_id column (left over from old deleted migrations)
        migrations.RunSQL(
            sql="ALTER TABLE blog_blog DROP COLUMN IF EXISTS account_id;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Make image nullable to match model (was NOT NULL in legacy schema)
        migrations.RunSQL(
            sql="ALTER TABLE blog_blog ALTER COLUMN image DROP NOT NULL;",
            reverse_sql="ALTER TABLE blog_blog ALTER COLUMN image SET NOT NULL;",
        ),
        # Change rating from varchar to integer to match model IntegerField
        migrations.RunSQL(
            sql="ALTER TABLE blog_review ALTER COLUMN rating TYPE integer USING rating::integer;",
            reverse_sql="ALTER TABLE blog_review ALTER COLUMN rating TYPE character varying(10) USING rating::character varying(10);",
        ),
        # Make review.user_id nullable to match model
        migrations.RunSQL(
            sql="ALTER TABLE blog_review ALTER COLUMN user_id DROP NOT NULL;",
            reverse_sql="ALTER TABLE blog_review ALTER COLUMN user_id SET NOT NULL;",
        ),
        # Change review.user_id from integer to bigint to match BigAutoField User PK
        migrations.RunSQL(
            sql="ALTER TABLE blog_review ALTER COLUMN user_id TYPE bigint USING user_id::bigint;",
            reverse_sql="ALTER TABLE blog_review ALTER COLUMN user_id TYPE integer USING user_id::integer;",
        ),
        # Add unique_together(user, blog) constraint if it doesn't already exist
        migrations.RunSQL(
            sql="""
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
            """,
            reverse_sql="ALTER TABLE blog_review DROP CONSTRAINT IF EXISTS blog_review_user_id_blog_id_uniq;",
        ),
    ]
