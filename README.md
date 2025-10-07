# puppygraph-demo

## 1 Create services

Create containers

```
docker compose up 
```

## 2 Seed data

Migrate tables using file `mock_data/clickhouse_mock_2.sql`, execute raw sql onto Clickhouse.

Generate seed data using file `mock_data/generate_customer_data.py`. It will create SQL Insert files.

## 3 Create db connection in Puppygraph

connect to Puppygraph via `localhost:8081`, use username and password as "admin".

1. Choose menu `Schema`, then click upload graph schema JSON.
2. Choose the file `puppygraph/schema.json` and click "**Upload**".

The database connection is already defined in the schema.json file. here is example.

```json
"catalogs": [
  {
    "name": "customer_domain",
    "type": "clickhouse",
    "jdbc": {
      "username": "admin",
      "password": "admin",
      "jdbcUri": "jdbc:clickhouse://clickhouse-server:8123/customer_domain",
      "driverClass": "com.clickhouse.jdbc.ClickHouseDriver",
      "enableMetaCache": "true",
      "metaCacheExpireSec": "600"
    }
  }
],
```