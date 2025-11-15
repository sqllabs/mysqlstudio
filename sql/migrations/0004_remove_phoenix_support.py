from django.db import migrations, models


DB_TYPE_CHOICES = [
    ("mysql", "MySQL"),
    ("redis", "Redis"),
    ("pgsql", "PgSQL"),
    ("mongo", "Mongo"),
    ("odps", "ODPS"),
    ("clickhouse", "ClickHouse"),
    ("goinception", "goInception"),
    ("cassandra", "Cassandra"),
    ("doris", "Doris"),
    ("elasticsearch", "Elasticsearch"),
    ("opensearch", "OpenSearch"),
    ("memcached", "Memcached"),
]


def check_phoenix_usage(apps, schema_editor):
    Instance = apps.get_model("sql", "Instance")
    ParamTemplate = apps.get_model("sql", "ParamTemplate")

    instance_count = Instance.objects.filter(db_type="phoenix").count()
    template_count = ParamTemplate.objects.filter(db_type="phoenix").count()

    if instance_count or template_count:
        details = []
        if instance_count:
            details.append(f"{instance_count} Phoenix instance(s)")
        if template_count:
            details.append(f"{template_count} Phoenix parameter template(s)")
        raise RuntimeError(
            "Phoenix removal blocked: "
            + ", ".join(details)
            + ". Please migrate or delete these records before applying this migration."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("sql", "0003_remove_mssql_support"),
    ]

    operations = [
        migrations.RunPython(check_phoenix_usage, migrations.RunPython.noop),
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
