#!/usr/bin/env python3

from dbprovider import database
import os


try:
    os.remove("main.db")
except:
    print("Removing file failed")
    pass

db = database()
db.build_tables()
print("Built tables")

db.put_hole(13231, 123, 456)
db.put_hole(13232, 789, 000)
print("Added holes")
print(db.get_holes())
print("Got holes")

db.put_segment(13231, 1, "GOP", 0, 10 )
db.put_segment(13231, 0, "", 10, 20 )
print("Added segments")
print(db.get_segments(13231))
print(db.get_segments(13232))
print("Got segments")

db.put_ply(13231, 1, "GOP", 0, 5 )
db.put_ply(13231, 1, "GOP1", 5, 10 )
print("Added ply")
print(db.get_ply(13231, 1))
print(db.get_ply(13231, 2))
print("Got ply")
