# Module python for Db operation

import sqlite3 as sql

# function to return the name of all the files saved in the db

def view():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("select * from files")
	files = cur.fetchall()
	print (files)
	con.close()
	return files

def delete(name):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("DELETE FROM files WHERE name='" + name + "'")
	con.commit()
	con.close()

def insert(name):
	con = sql.connect("database.db")
	cur = con.cursor()
	try:
		cur.execute('DELETE FROM files WHERE name="'+name+'"')
	except:
		pass
	cur.execute("insert into files(name) values ('"+ name + "')")
	con.commit()
