data = {
    'id' : '202010',
    'name': 'Bob',
    'age': '20'
}

table = 'Students'
keys = ','.join(data.keys())
values = ','.join(['%s'] * len(data))
values
## old formating method
sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table = table, keys = keys, values = values) %tuple(data.values())
sql

values2 = ','.join(['{}'] * len(data))
values2
## new formating method                                                          ## unpack list using the * operator.
sql2 = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table = table, keys = keys, values = values2).format(*list(data.values()))
sql2


list(data.values())
tuple(data.values())

try:
    if cursor.execute(sql, tuple(data.values())):
        print('Successful')
        db.commit()
    except:
        db.rollback()
    db.close()
