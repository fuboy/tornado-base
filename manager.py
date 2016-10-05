import sys
from project import make_app
from project.core.config import Config

functions = ['routes', 'create_db', 'drop_db', 'create_schema', 'populate_db', 'auto_code']


def routes(app):
    for url_spec in app.handlers[0][1]:
        print 'route name = %r, pattern = %r, handler_name = %s'%\
            (url_spec.name, url_spec.regex.pattern,
             url_spec.handler_class) #, url_spec.kwargs)


def create_db(app):
    from project.core.db import db
    from sqlalchemy_utils import database_exists, create_database
    if not database_exists(db.engine.url):
        print '====> Create database'
        create_database(db.engine.url)
    else:
        print '====> database exist'


def drop_db(app):
    from project.core.db import db
    from sqlalchemy_utils import database_exists, drop_database
    if database_exists(db.engine.url):
        print '====> Drop database'
        drop_database(db.engine.url)
    else:
        print '====> database not exist'


def create_schema(app):
    from project.core.db import db
    db.BaseModel.metadata.create_all(db.engine)
    print '===> Create schema <==='


def auto_code_module(module_dir, user_types):
    model_file = open(module_dir, 'r')

    acl_field = {}
    acl_user = {}

    for t in user_types:
        acl_user[t] = []

    dft_view = {}

    supported = False
    new_lines = ''
    lines = model_file.readlines()
    model_file.close()

    for i in range(len(lines)):
        line = lines[i]
        if line == '\n' or line == '':
            new_lines += line
            continue
        elif '### others ###' in line:
            new_lines += line
            ### email: acl[*] # default
            i += 1
            line = lines[i]
            while '### END_OTHERS ###' not in line:
                line = line.split(':')

                field_name = line[0].strip(' ').split('###')[1].strip(' ')
                line = line[1].split('#')

                # acl
                acl = line[0].split('[')[1].strip(' ').split(']')[0]
                if field_name not in acl_field:
                    acl_field[field_name] = []
                if acl == '*':
                    for t in user_types:
                        acl_field[field_name].append(t)
                        acl_user[t].append(field_name)
                else:
                    for t in acl.split(','):
                        t = t.strip(' ')
                        if t == '':
                            continue
                        acl_field[field_name].append(t)
                        acl_user[t].append(field_name)
                # end acl

                # dft
                if len(line) > 1:
                    dft = line[1].strip(' ').split('[')
                    if len(dft) > 1:
                        dft = dft[1].strip(' ').split(']')[0]
                        dft_view[field_name] = dft
                    else:
                        dft_view[field_name] = field_name
                # end dft

                i += 1
                line = lines[i]

        elif line.strip(' ').startswith('# acl'):
            new_lines += line
            i += 1
            field_name = lines[i].strip(' ').split('=')[0].strip(' ')

            line = line.strip(' ').split('\n')[0].strip(' ').split('#')[1:]

            # acl
            acl = line[0].split('[')[1].strip(' ').split(']')[0]
            if field_name not in acl_field:
                acl_field[field_name] = []
            if acl == '*':
                for t in user_types:
                    acl_field[field_name].append(t)
                    acl_user[t].append(field_name)
            else:
                for t in acl.split(','):
                    t = t.strip(' ')
                    if t == '':
                        continue
                    acl_field[field_name].append(t)
                    acl_user[t].append(field_name)
            # end acl

            # dft
            if len(line) > 1:
                dft = line[1].strip(' ').split('[')
                if len(dft) > 1:
                    dft = dft[1].strip(' ').split(']')[0]
                    dft_view[field_name] = dft
                else:
                    dft_view[field_name] = field_name
            # end dft

        elif line == '### auto_generate_support ###\n' or line == '### auto_generate_support ###':
            supported = True
            new_lines += line
        elif '# auto generate' in line:
            # new_lines += line
            # new_lines += '# end auto generate\n'
            break
        else:
            new_lines += line

    # print acl_field
    # print acl_user
    # print dft_view
    # print new_lines

    if supported:

        new_lines += '    # auto generate\n'

        acl_field['id'] = []
        acl_field['created_at'] = []
        acl_field['updated_at'] = []

        for t in user_types:
            acl_user[t].append('id')
            acl_user[t].append('created_at')
            acl_user[t].append('updated_at')

            acl_field['id'].append(t)
            acl_field['created_at'].append(t)
            acl_field['updated_at'].append(t)

        new_lines += '    @classmethod\n'
        new_lines += '    def acl(cls):\n'
        new_lines += '        return {\n'
        for key, value in acl_field.iteritems():
            new_lines += '            \'' + key + '\': [' + ', '.join(['\'' + v + '\'' for v in value]) + '],\n'
        new_lines += '        }\n'

        new_lines += '\n'
        new_lines += '    @classmethod\n'
        new_lines += '    def user_acl(cls):\n'
        new_lines += '        return {\n'
        for key, value in acl_user.iteritems():
            new_lines += '            \'' + key + '\': [' + ', '.join(['\'' + v + '\'' for v in value]) + '],\n'
        new_lines += '        }\n'

        dft_view['id'] = 'id'
        dft_view['created_at'] = 'created_at'
        dft_view['updated_at'] = 'updated_at'

        new_lines += '\n'
        new_lines += '    @classmethod\n'
        new_lines += '    def dft_view(cls):\n'
        new_lines += '        return {\n'
        for key, value in dft_view.iteritems():
            new_lines += '            \'' + key + '\': \'' + value + '\',\n'
        new_lines += '        }\n'

        new_lines += '    # end auto generate\n'

    # save to file
    model_file = open(module_dir, 'w')
    model_file.write(new_lines)


def auto_code(app, module_name=None):
    if module_name:
        if len(module_name.split('.')) > 1:
            h_module = module_name.split('.')
            module_name = ''
            for m in h_module:
                module_name += m + '/'

            module_name = module_name[:-1]

        module_dir = 'project/modules/' + module_name + '/models.py'
        auto_code_module(module_dir, app.settings['user_types'])
    else:
        for name, module in app.settings['modules'].iteritems():
            if module == 'auth':
                continue
            if len(module.split('.')) > 1:
                h_module = module.split('.')
                module = ''
                for m in h_module:
                    module += m + '/'

                module = module[:-1]

            module_dir = 'project/modules/' + module + '/models.py'
            auto_code_module(module_dir, app.settings['user_types'])


def populate_db(app):
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '=> You can pass --help to see help of manager <='
    elif '--help' in sys.argv:
        print 'Help: exist functions'
        i = 1
        for func_name in functions:
            print '{index}. {func_name}'.format(index=i, func_name=func_name)
            i += 1
    elif sys.argv[1] not in functions:
        print 'Error:=> calling function irregular!!! call command with --help \n'
    else:
        app = make_app(Config)
        func_name = sys.argv[1]
        if func_name == 'routes':
            print '===>Call routes function:<==='
            routes(app)
        elif func_name == 'create_db':
            print '===>Call create_db function:<==='
            create_db(app)
        elif func_name == 'create_schema':
            print '===>Call create_schema function:<==='
            create_schema(app)
        elif func_name == 'drop_db':
            print '===>Call drop_db function:<==='
            drop_db(app)
        elif func_name == 'populate_db':
            print '===>Call populate_db function:<==='
            populate_db(app)
        elif func_name == 'auto_code':
            print '===>Call auto_code function:<==='
            module_name = sys.argv[2] if len(sys.argv) > 2 else None
            auto_code(app, module_name)


