from django.db import migrations, models


DB_TYPE_CHOICES = [
    ("mysql", "MySQL"),
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


def ensure_no_mssql_instances(apps, schema_editor):
    Instance = apps.get_model("sql", "Instance")
    if Instance.objects.filter(db_type="mssql").exists():
        raise RuntimeError(
            "MsSQL support has been removed. Please migrate or delete all MsSQL "
            "instances before applying this migration."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("sql", "0002_remove_oracle_support"),
    ]

    operations = [
        migrations.RunPython(
            ensure_no_mssql_instances, migrations.RunPython.noop
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
