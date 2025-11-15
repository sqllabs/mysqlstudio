from django.db import migrations, models


DB_TYPE_CHOICES = [
    ("mysql", "MySQL"),
    ("mssql", "MsSQL"),
    ("redis", "Redis"),
    ("pgsql", "PgSQL"),
    ("mongo", "Mongo"),
    ("phoenix", "Phoenix"),
    ("odps", "ODPS"),
    ("clickhouse", "ClickHouse"),
    ("goinception", "goInception"),
    ("cassandra", "Cassandra"),
    ("doris", "Doris"),
    ("elasticsearch", "Elasticsearch"),
    ("opensearch", "OpenSearch"),
    ("memcached", "Memcached"),
]


class Migration(migrations.Migration):

    dependencies = [
        ("sql", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="instance",
            name="service_name",
        ),
        migrations.RemoveField(
            model_name="instance",
            name="sid",
        ),
        migrations.AlterField(
            model_name="instance",
            name="db_type",
            field=models.CharField(
                "数据库类型", max_length=20, choices=DB_TYPE_CHOICES
            ),
        ),
        migrations.AlterField(
            model_name="paramtemplate",
            name="db_type",
            field=models.CharField(
                "数据库类型", max_length=20, choices=DB_TYPE_CHOICES
            ),
        ),
    ]
