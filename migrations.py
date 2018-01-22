
def make_migrate():
    print("MIGRATION")
    from Common.models import migrator

    from playhouse.migrate import migrate, CharField, FloatField

    migrations = [('ProviderOrClient', 'devise', CharField(default="xof")),
                  ('Payment', 'weight', FloatField(default="0"))]

    for x, y, z in migrations:
        try:
            migrate(migrator.add_column(x, y, z))
            print(x, " : ", y)
        except Exception as e:
            print(e)
