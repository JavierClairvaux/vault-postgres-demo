# vault-postgres-demo

This is a demo to show the capabilities of Vault's database dynamic credentials.

Demo assumes you have the Vault and Python 3 installed.

As this is made for demo porpouses it's not meant to be used in development.

To start the demo run:
```bash
docker compose up vault database
```

This will start the database and Vault containers.

To populate the database run
```bash
python3 postgresql.py; python3 inset-data.py
```

Then create a RO role for this database
```bash
docker exec -i \
    sampledb \
    psql -U postgres -c "CREATE ROLE \"ro\" NOINHERIT;"
```

Grant reading on all tables to this role
```bash
docker exec -i \
    sampledb \
    psql -U postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"ro\";"
```

Export Vault related environment variables
```bash
export VAULT_ADDR='http://127.0.0.1:8200'; export VAULT_TOKEN=root 
```

Add PostgresQL URL environment variable
```bash
export POSTGRES_URL=sampledb:5432
```

Enable database secrets engine
```bash
vault secrets enable database
```

Write database's configuration to Vault
```bash
vault write database/config/postgresql\ 
     plugin_name=postgresql-database-plugin \
     connection_url="postgresql://{{username}}:{{password}}@$POSTGRES_URL/postgres?sslmode=disable" \
     allowed_roles=readonly \
     username="postgres" \
     password="default"
```

Configure readonly role
```bash
vault write database/roles/readonly \
      db_name=postgresql \
      creation_statements=@readonly.sql \
      default_ttl=1h \
      max_ttl=24h
```

Optional: read credentials to prove configuration and role are working
```bash
vault read database/creds/readonly
```

Optional: revoke all leases
```bash
vault lease revoke -prefix database/creds 
```

On the template `readonly.sql` you can see the role assigned to the credentials that will be generated. In this case we are assigned the role we created above RO

Once Vault and the database are configured start the web service
```bash
docker compose up web
```

Check service is running correctly at [http://127.0.0.1:5000](http://127.0.0.1:5000).

Get the lease id created by the service
```bash
vault list sys/leases/lookup/database/creds/readonly
```

Revoke the lease
```bash
vault lease revoke database/creds/readonly/<lease id obtained from the last step>
```

Refresh [http://127.0.0.1:5000](http://127.0.0.1:5000) to verify credentials aren't working anymore.

Restart container to refresh credentials
```bash
docker compose restart web
```

Refresh [http://127.0.0.1:5000](http://127.0.0.1:5000) to ensure website is working again.