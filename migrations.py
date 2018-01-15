
def v001():
    print("MIGRATION")
    from Common.models import migrator

    from playhouse.migrate import migrate, CharField

    migrate(
        migrator.add_column('ProviderOrClient', 'devise',
                            CharField(default="xof")),
    )


def init():

    try:
        v001()
    except:
        pass
