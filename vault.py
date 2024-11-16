import hvac
import psycopg2

client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='root',
)

def getData(database, user, password):
    conn = psycopg2.connect(database = database, 
                        user = user, 
                        host= 'localhost',
                        password = password,
                        port = 5432)

    cur = conn.cursor()
    cur.execute('SELECT * FROM datacamp_courses;')
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# read_response = client.secrets.kv.read_secret_version(path='my-secret')

# # password = read_response['data']['data']['password']

# print('Value under path "secret/foo" / key "foo": {val}'.format(val=read_response['data']['data']['foo'],))

credentials = client.secrets.database.generate_credentials(
    name='readonly',
    mount_point='database'
)



print(credentials)

rows = getData("postgres", credentials['data']['username'], credentials['data']['password'])

print(rows)