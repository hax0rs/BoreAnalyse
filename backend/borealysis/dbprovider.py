#!/usr/bin/env python3

import sqlite3

class database:

    dbfile = "main.db"

    # HOLE: ID us correlating to the real data
    # SECTION: ID gives order (1 top, 2 middle, 3 bottom)
    #  Start and end range are in cm
    # PLY: ID gives order (1 top, 2 middle, 3 bottom)
    #  Start and end range are in cm

    tables = [
        """CREATE TABLE holes
        (id integer,
        lat real,
        lon real)""",

        """CREATE TABLE segments
        (id integer,
        bid integer,
        seam BOOLEAN,
        sectype text,
        startrange integer,
        endrange integer)""",

        """CREATE TABLE plys
        (id integer,
        bid integer,
        sid integer,
        plytype text,
        startrange integer,
        endrange integer)"""
              ]

    conn = None
    c = None

    def __init__(self):
        # FIXME: WHAT COULD GO WRONG?
        self.conn = sqlite3.connect(self.dbfile, check_same_thread=False)
        self.c = self.conn.cursor()

    def build_tables(self):
        for table_string in self.tables:
            self.c.execute(table_string)
        self.conn.commit()

    def run_query(self, qstring):
        return list(self.c.execute(qstring))

    def write_query(self, qstring):
        self.c.execute(qstring)
        self.conn.commit()

    def get_holes(self):
        return self.run_query("""SELECT id, lat, lon
                              FROM holes""")
    def get_hole(self, holeid):
        return self.run_query("""SELECT id, lat, lon
                              FROM holes
                              WHERE id={}""".format(holeid))

    def get_hole_depth(self, holeid):
        return self.run_query("""SELECT max(endrange)
                              FROM segments
                              WHERE bid={}""".format(holeid))

    def get_hole_stats(self, holeid, segtype):
        return self.run_query("""SELECT COUNT(*), SUM((endrange-startrange))
                              FROM segments
                              GROUP BY bid, sectype
                              HAVING bid={} AND sectype='{}'""".format(holeid, segtype))

    def get_hole_breakdown(self, holeid):
        return self.run_query("""SELECT sectype, COUNT(*), SUM((endrange-startrange))
                              FROM segments
                              GROUP BY bid, sectype
                              HAVING bid={} AND seam = 1
                              ORDER BY SUM((endrange-startrange))""".format(holeid))

    # fixme: sql injection is possible
    def get_segments(self, holeid):
        return self.run_query("""select id, seam, sectype, startrange, endrange
                              from segments
                              where bid={}""".format(holeid))

    # fixme: sql injection is possible
    def get_segment(self, holeid, segid):
        return self.run_query("""select id, seam, sectype, startrange, endrange
                              from segments
                              where bid={} AND id={}""".format(holeid, segid))

    # FIXME: SQL INJECTION IS POSSIBLE
    def get_plys(self, holeid, segmentid):
        return self.run_query("""SELECT id, plytype, startrange, endrange
                              FROM plys
                              WHERE bid={} AND sid={}""".format(holeid, segmentid))

    # FIXME: SQL INJECTION IS POSSIBLE
    def put_hole(self, holeid, lat, lon):
        return self.write_query("""INSERT INTO holes
                              VALUES({}, {}, {})""".format(holeid, lat, lon))

    # FIXME: SQL INJECTION IS POSSIBLE
    def put_segment(self, holeid, seam, seamtype, startrange, endrange):
        return self.write_query( """INSERT INTO segments
                         VALUES((SELECT IFNULL(MAX(id), 0)+1 FROM segments WHERE bid={}), {}, {}, '{}', {}, {})
                         """.format(holeid, holeid, seam, seamtype, startrange, endrange))

    # FIXME: SQL INJECTION IS POSSIBLE
    def put_ply(self, holeid, segid, seamtype, startrange, endrange):
        return self.write_query("""INSERT INTO plys
                              VALUES((SELECT IFNULL(MAX(id), 0)+1 FROM plys WHERE bid={} AND sid={}), {}, {}, '{}', {}, {})
                              """.format(holeid, segid, holeid, segid, seamtype, startrange, endrange))
