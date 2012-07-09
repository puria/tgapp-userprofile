from tg import expose

@expose('userprofile.templates.little_partial')
def something(name):
    return dict(name=name)