from pytest_mock import MockFixture

from common.config import SysConfig
from sql.engines.doris import DorisEngine
from sql.engines.models import ResultSet


def test_doris_server_info(db_instance, mocker: MockFixture):
    mock_query = mocker.patch.object(DorisEngine, "query")
    mock_query.return_value = ResultSet(
        full_sql="show frontends", rows=[["foo", "bar", "2.1.0-doris"]]
    )
    db_instance.db_type = "doris"
    engine = DorisEngine(instance=db_instance)
    version = engine.server_version
    assert version == (2, 1, 0)


def test_forbidden_db(db_instance, mocker: MockFixture):
    db_instance.db_type = "doris"
    mock_query = mocker.patch.object(DorisEngine, "query")
    mock_query.return_value = ResultSet(
        full_sql="show databases", rows=[["__internal_schema"]]
    )

    engine = DorisEngine(instance=db_instance)
    all_db = engine.get_all_databases()
    assert all_db.rows == []


def test_execute_check_critical_regex_partial(db_instance):
    db_instance.db_type = "doris"
    config = SysConfig()
    original = config.get("critical_ddl_regex", "")
    regex = r"(?i)drop\s+column"
    config.set("critical_ddl_regex", regex)
    config.get_all_config()
    engine = DorisEngine(instance=db_instance)
    sql = "alter table users drop column email"
    result = engine.execute_check(db_name="test_db", sql=sql)
    assert result.rows[0].stagestatus == "Rejected critical SQL"
    assert (
        result.rows[0].errormessage
        == "Submitting statements matching " + regex + " is forbidden."
    )
    config.set("critical_ddl_regex", original or "")
    config.get_all_config()
