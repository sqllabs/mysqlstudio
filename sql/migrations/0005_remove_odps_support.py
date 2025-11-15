from django.db import migrations, models


DB_TYPE_CHOICES = [
    ("mysql", "MySQL"),
    ("redis", "Redis"),
    ("pgsql", "PgSQL"),
    ("mongo", "Mongo"),
    ("clickhouse", "ClickHouse"),
    ("goinception", "goInception"),
    ("cassandra", "Cassandra"),
    ("doris", "Doris"),
    ("elasticsearch", "Elasticsearch"),
    ("opensearch", "OpenSearch"),
    ("memcached", "Memcached"),
]


def check_odps_usage(apps, schema_editor):
    Instance = apps.get_model("sql", "Instance")
    ParamTemplate = apps.get_model("sql", "ParamTemplate")

    instance_count = Instance.objects.filter(db_type="odps").count()
    template_count = ParamTemplate.objects.filter(db_type="odps").count()

    if instance_count or template_count:
        details = []
        if instance_count:
            details.append(f"{instance_count} ODPS instance(s)")
        if template_count:
            details.append(f"{template_count} ODPS parameter template(s)")
        raise RuntimeError(
            "ODPS support removal blocked: "
            + ", ".join(details)
            + ". Please migrate or delete these records before applying this migration."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("sql", "0004_remove_phoenix_support"),
    ]

    operations = [
        migrations.RunPython(check_odps_usage, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="instance",
            name="db_type",
            field=models.CharField(
                "数据库类型",
                max_length=20,
                choices=DB_TYPE_CHOICES,
            ),
        ),
        migrations.AlterField(
            model_name="paramtemplate",
            name="db_type",
            field=models.CharField(
                "数据库类型",
                max_length=20,
                choices=DB_TYPE_CHOICES,
            ),
        ),
    ]
