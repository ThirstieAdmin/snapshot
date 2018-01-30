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
