from pgactivity.Data import Data
import sys, re
import getopt

config = {
    'host': '',
    'database': '',
    'logdb': '',
    'logfile': '',
    'mem_percent_max': 5,
    'cpu_percent_max': 1 
}


def dump(proc_id, cpu_percent, mem_percent, query_start, query, prev_queries): 
    print '################## PostgreSQL query #######################'
    print 'Query: {query}'.format(**locals())
    print 'ID: {} CPU: {} MEM: {} START: {}'.format(proc_id, cpu_percent, mem_percent, query_start)
    for query in prev_queries:
        if len(query) > 0:
            print 'START: {} {} QUERY: {}'.format(query[0], query[1], query[3]) 

def main(config, skip_idle):
    db = Data()
    db.pg_connect(
        host = config['host'],
        database = config['database'] 
    )

    pg_version = db.pg_get_version()
    waiting_queries = db.pg_get_waiting()
    blocking_queries =  db.pg_get_blocking()
    active_queries =  db.pg_get_activities()
    active_procs = db.sys_get_proc(active_queries, True)
    n_active_procs = len(active_procs)
    for proc_id in active_procs:
        proc = active_procs[proc_id]
        query = active_procs[proc_id].query
        query_start = active_procs[proc_id].query_start
        mem_percent = proc.extras['mem_percent']
        cpu_percent = proc.extras['cpu_percent']

        if proc.query.startswith('<IDLE>') and skip_idle:
            n_active_procs -= 1
            continue
        if cpu_percent >= config['cpu_percent_max'] or mem_percent >= config['mem_percent_max'] or not skip_idle:
            with open(config['logfile'], 'r') as log:
                prev_queries = []
                for line in log:
                    regex_syntax = "(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) CEST %s \((%s)/\d+\) LOG: (.*)" % (config['logdb'],proc_id)
                    regex = re.compile(regex_syntax)
                    match = regex.match(line)
                    if match:
                        prev_queries.append(match.groups())
                dump(proc_id, cpu_percent, mem_percent, query_start, query, prev_queries) 
    print 'Active procs: {}'.format(n_active_procs)
    status = False
    if n_active_procs == 0:
        status = True 
    print 'Status (test): {}'.format(status) 

if __name__ == '__main__':
    argv = sys.argv[1:]
    skip_idle = False 
    try:
        opts, args = getopt.getopt(argv,"h",["skip-idle"])
    except getopt.GetoptError:
      print 'monitor.py <--skip-idle>'
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'monitor.py <--skip-idle>'
        elif opt == '--skip-idle':
            skip_idle = True 
    main(config, skip_idle)
