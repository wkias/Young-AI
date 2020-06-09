import sqlite3


class sqliteDB:

    def __init__(self, table, db='face.db'):
        self.table = table
        self.sql = {}
        self.sql['create'] = {}
        self.sql['insert'] = {}
        self.sql['create']['face'] = '''
            create table if not exists {0}(
                        face_token      text        prime key   not null,
                        time            timestamp,
                        age             integer,
                        beauty          real,
                        expression      text,
                        face_shape      text,
                        gender          text,
                        glasses         text,
                        race            text,
                        blur            real,
                        illumination    real,
                        completeness    integer,
                        emotion         text,
                        face_type       text,
                        json            blob,
                        img_hash        text
                        )'''.format(self.table)
        self.sql['create']['face_probability'] = '''
            create table if not exists {0}(
                        face_token      text        prime key   not null,
                        face            real,
                        age             integer,
                        beauty          real,
                        expression      real,
                        face_shape      real,
                        gender          real,
                        glasses         real,
                        race            real,
                        emotion         real,
                        face_type       real
                        )'''.format(self.table)
        self.sql['create']['img'] = '''
            create table if not exists {0}(
                        img_hash        text,
                        bytes_img       blob
                        )'''.format(self.table)
        self.sql['insert']['face'] = '''
            insert into {0} values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            '''.format(self.table)
        self.sql['insert']['face_probability'] = '''
            insert into {0} values (?,?,?,?,?,?,?,?,?,?,?)
            '''.format(self.table)
        self.sql['insert']['img'] = '''
            insert into {0} values (?,?)
            '''.format(self.table)
        self.sql['delete'] = 'delete from {0} where %s'.format(self.table)
        self.sql['select'] = 'select * from {0}'.format(self.table)
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(self.sql['create'][self.table])

    def insert(self, content):
        self.cur.execute(self.sql['insert'][self.table], content)
        self.conn.commit()

    def delete(self, condition):
        self.cur.execute(self.sql['delete'] % condition)
        self.conn.commit()

    def select(self, items='*', condition=None):
        command = self.sql['select']
        if condition is not None:
            command = command + ' where ' + condition
        return self.cur.execute(command)

    def close(self):
        self.conn.close()
