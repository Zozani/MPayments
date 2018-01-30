
def make_migrate():
    print("aditional list")

    from playhouse.migrate import CharField

    return [('ProviderOrClient', 'devise', CharField(default="xof")), ]
