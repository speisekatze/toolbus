import sqlite3

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
    host = {'ip': '', 'stage': 0, 'uid': '', 'hostname': '', 'group': '', 'empty': True}
    if host_info is not None:
        host['ip'] = host_info[3]
        host['stage'] = host_info[5]
        host['uid'] = host_info[1]
        host['hostname'] = host_info[4]
        host['group'] = host_info[2]
        host['empty'] = False
    return host

def get_next_stage(stage):
    stage += 1
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    r = cur.execute(f"SELECT * FROM flow WHERE sort = {stage}")
    flow_info = r.fetchone()
    if flow_info is None:
        r = cur.execute("SELECT * FROM flow WHERE sort = (SELECT MAX(sort) FROM flow)")
        flow_info = r.fetchone()
    con.close()
    return flow_info

def update_group(id, serial):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    cur.execute(f"UPDATE groups SET serial = {serial} WHERE id = {id}")
    con.commit()
    con.close()

def update_stage(host):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    cur.execute(f"UPDATE hosts SET stage = {host['stage']} WHERE uid = '{host['uid']}'")
    con.commit()
    con.close()

def new_host(host):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    cur.execute(f"INSERT INTO hosts(uid, `group`, ip, hostname, stage) VALUES('{host['uid']}', {host['group']}, '{host['ip']}', '{host['hostname']}', {host['stage']} )")
    con.commit()
    con.close()

def get_ips_from_group(groupid):
    con = sqlite3.connect('inventory/hosts.sqlite')
    cur = con.cursor()
    r = cur.execute(f"SELECT ip FROM hosts WHERE `group` = {groupid}")
    ips = r.fetchall()
    con.close()
    return [x[0] for x in ips]