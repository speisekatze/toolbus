import os.path
import sqlite3

def get_script(name):
    filename = f'scripts/{name}.toolbus'
    if not os.path.isfile(filename):
        return ''
    with open(filename, 'r') as f:
        lines = f.readlines()
    return "\n".join(lines)

def get_group(name):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    r = cur.execute(f"SELECT * FROM groups WHERE name = '{name}'")
    group_info = r.fetchone()
    con.close()
    return group_info

def get_host(uid):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    r = cur.execute(f"SELECT * FROM hosts WHERE uid = '{uid}'")
    host_info = r.fetchone()
    con.close()
    return host_info

def get_next_stage(stage):
    stage += 1
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    r = cur.execute(f"SELECT * FROM flow WHERE sort = {stage}")
    flow_info = r.fetchone()
    con.close()
    return flow_info

def update_group(id, serial):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    cur.execute(f"UPDATE groups SET serial = {serial} WHERE id = {id}")
    con.commit()
    con.close()

def new_host(host):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    cur.execute(f"INSERT INTO hosts(uid, group, ip, hostname, stage) VALUES('{host['uid']}', {host['group']}, '{host['ip']}', '{host['hostname']}', {host['stage']} )")
    con.commit()
    con.close()