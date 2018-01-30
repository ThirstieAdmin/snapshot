'''
usage: snapshot [-h] [--host HOST] [--port PORT] [--database DATABASE]
                     [--user USER] [--password PASSWORD]
                     [--table-prefix PREFIX]
                     [--updates [UPDATES [UPDATES ...]]]
                     command

Save and restore MySQL databases

positional arguments:
  command               a command to run

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           database host
  --port PORT           database port
  --database DATABASE   database name
  --user USER           database user
  --password PASSWORD   database password
  --table-prefix PREFIX
                        backup tables starting with PREFIX
  --updates [UPDATES [UPDATES ...]]
                        SQL query file to apply after restore
'''

import subprocess


def backup(host, port, database, user, password, table_prefix=None):
    if table_prefix is not None:
        command = ['mysql', database, '-NB', '-h', host, '-P', port, '-u', user, '-p%s' % password, '-e', 'SHOW TABLES LIKE \'{0}%\''.format(table_prefix)]
        qry_proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            outs, errs = qry_proc.communicate(timeout=30)
        except TimeoutExpired:
            proc.kill()
            outs, errs = qry_proc.communicate()

        if outs:
            tables = outs.decode('ascii').strip().split('\n')
            mysqldump(host, port, user, password, database, tables)
    else:
        mysqldump(host, port, user, password, database)

def mysqldump(host, port, user, password, database, tables=None):
    command = ['mysqldump', '-h', host, '-P', port, '-u', user, '-p%s' % password, database]

    if tables is not None:
        command += tables

    subprocess.run(command)

def load(host, port, user, password, database):
    command = ['mysql', '-h', host, '-P', port, '-u', user, '-p%s' % password, database]
    subprocess.run(command)

def update(host, port, user, password, database, infile):
    command = ['mysql', '-h', host, '-P', port, '-u', user, '-p%s' % password, database]
    subprocess.run(command, input=infile.read())


# if __name__ == '__main__':
#     import argparse
# 
#     parser = argparse.ArgumentParser(description='Save and restore MySQL databases')
#     parser.add_argument('command', type=str, help='a command to run')
#     parser.add_argument('--host', dest='host', type=str, help='database host')
#     parser.add_argument('--port', dest='port', default='3306', type=str, help='database port')
#     parser.add_argument('--database', dest='database', type=str, help='database name')
#     parser.add_argument('--user', dest='user', type=str, help='database user')
#     parser.add_argument('--password', dest='password', type=str, help='database password')
# 
#     # Arguments for backups
#     parser.add_argument('--table-prefix', dest='prefix', default=None, type=str, help='backup tables starting with PREFIX')
# 
#     # Arguments for restores
#     parser.add_argument('--updates', dest='updates', nargs='*', type=argparse.FileType('rb'), help='SQL query file to apply after restore')
# 
#     args = parser.parse_args()
# 
#     if args.command == 'backup':
#         print('Backing up mysql://%s:%s/%s ...' % (args.host, args.port, args.database), file=sys.stderr)
#         backup(args.host, args.port, args.database, args.user, args.password, table_prefix=args.prefix)
#     elif args.command == 'restore':
#         print('Restoring mysql://%s:%s/%s ...' % (args.host, args.port, args.database), file=sys.stderr)
#         load(args.host, args.port, args.user, args.password, args.database)
# 
#         if args.updates:
#             print('Running update scripts ...', file=sys.stderr)
#             for file in args.updates:
#                 update(args.host, args.port, args.user, args.password, args.database, file)
