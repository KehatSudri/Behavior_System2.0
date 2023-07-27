import datetime
import logging
import sys
import psycopg2
from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def config(filename):
    section = 'postgresql'
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section "postgresql" not found in file: {format(section, filename)}')
    return db


class DB:
    _instance = None

    def __new__(cls, filename=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if filename is not None:
                cls._instance.initialize(filename)
        return cls._instance

    def initialize(self, filename):
        db_config = config(filename)
        self.db_name = db_config['database']
        db_config['database'] = 'postgres'
        self.connect(db_config)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.create_db()
        db_config['database'] = self.db_name
        self.disconnect()
        self.connect(db_config)
        self.create_tables()
        self.insert_mock_events()

    def connect(self, params):
        """ Connect to the PostgresSQL database server """
        try:
            # connect to the PostgresSQL server
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            sys.exit()

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.db_name}'")
            exists = cur.fetchone()
            if exists is None:
                cur.execute('CREATE DATABASE "Behavior_sys"')

    def create_tables(self):
        with self.conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
            self.conn.commit()

    def insert_mock_events(self):
        sql = """INSERT INTO events(port, name, type, format, is_reward) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO 
        NOTHING"""
        with self.conn.cursor() as cur:
            cur.execute(sql, ("Tone", "Tone", "Output", "Analog", False))
            self.conn.commit()

    def insert_hardware_event(self, name, port, type, format, is_reward):
        try:
            sql = """INSERT INTO events(port, name, type, format, is_reward) VALUES (%s,%s,%s,%s,%s)"""
            with self.conn.cursor() as cur:
                cur.execute(sql, (name, port, type, format, is_reward))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def insert_session(self, name, subjectid, experimenter_name, last_used, min_iti,
                       max_iti, is_fixed_iti, max_trial_time, notes):
        try:
            sql = """INSERT INTO sessions(name,subjectid,experimenter_name,last_used,min_iti,max_iti,is_fixed_iti,
            max_trial_time,notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
            with self.conn.cursor() as cur:
                cur.execute(sql, (
                    name, subjectid, experimenter_name, last_used, min_iti, max_iti, is_fixed_iti, max_trial_time,
                    notes))
                self.conn.commit()
                row_id= cur.fetchone()[0]
            return row_id
        except Exception as e:
            self.conn.rollback()
            raise e

    def insert_session_to_trials(self, session_id, trial_name):
        sql = """INSERT INTO session_to_trials(session_id, trial_name) VALUES (%s,%s)"""
        with self.conn.cursor() as cur:
            cur.execute(sql, (session_id, trial_name))
            self.conn.commit()

    def insert_new_trial(self, name):
        try:
            sql = """INSERT INTO trials(name) VALUES (%s)"""
            with self.conn.cursor() as cur:
                cur.execute(sql, (name,))
        except Exception as e:
            self.conn.rollback()
            raise e

    def insert_new_events_to_trials(self, trial_name, event_name, is_contingent, contingent_on, isRandom,
                                    isEndCondition,preCondition):
        sql = """INSERT INTO events_to_trials(event_name, trial_name, is_contingent, contingent_on,israndom,
        isendcondition,preCondition) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        with self.conn.cursor() as cur:
            cur.execute(sql, (event_name, trial_name, is_contingent, contingent_on, isRandom, isEndCondition,preCondition))
            self.conn.commit()
    def getPreCondition(self,event,trial):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT preCondition FROM events_to_trials WHERE event_name='{event}' AND trial_name='{trial}'")
            preCondition = cur.fetchall()
        return preCondition

    def insert_session_trials(self, session_id, trial_type_id, percent_in_session=None,
                              percent_in_block=None, block_number=None, event_list=None, interval_list=None):
        sql = """INSERT INTO sessionTrials(session_id, trial_type_id, percent_in_session,percent_in_block, block_number,
                              event_list,interval_list) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING session_trial_id"""
        cur = self.conn.cursor()
        cur.execute(sql, (
            session_id, trial_type_id, percent_in_session, percent_in_block, block_number, event_list, interval_list))
        sess_trial_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return sess_trial_id

    def isEndConditionEvent(self, event_name, trial_name):
        with self.conn.cursor() as cur:
            sql = """SELECT isendcondition FROM events_to_trials WHERE event_name=%s AND trial_name=%s"""
            cur.execute(sql, (event_name, trial_name))
            isEndConditionEvent = cur.fetchone()
        return isEndConditionEvent

    def insert_event(self, event_type, parameters=None):
        sql = """INSERT INTO events(event_type, parameters) VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING event_id"""
        cur = self.conn.cursor()
        cur.execute(sql, (event_type, parameters))
        fetch = cur.fetchone()
        if cur.statusmessage != "INSERT 0 0":
            event_id = fetch[0]
        else:
            sql = """SELECT event_id FROM events WHERE event_type=%s AND parameters=%s"""
            cur.execute(sql, (event_type, parameters))
            event_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return event_id

    def insert_subject_session(self, subject_id, session_id, counter=0):
        sql = """INSERT INTO subjectSession(subject_id, session_id, counter,last_used) VALUES (%s,%s,%s,%s) 
                ON CONFLICT ON CONSTRAINT sbjsess_pkey DO UPDATE SET last_used=%s"""
        cur = self.conn.cursor()
        cur.execute(sql, (subject_id, session_id, counter, datetime.date.today(), datetime.date.today()))
        self.conn.commit()
        cur.close()
        self.conn.commit()

    def get_session_templates(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM sessions")
            sessions = cur.fetchall()
        return sessions

    def get_hardware_events(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM events")
            events = cur.fetchall()
        return events

    def get_hardware_events_by_name(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT name FROM events")
            names = cur.fetchall()
        return names

    def get_event_name_by_port_and_trial(self, port, trial):
        with self.conn.cursor() as cur:
            sql = f"SELECT name FROM events , events_to_trials WHERE port=%s AND events_to_trials.trial_name = %s "
            cur.execute(sql, (port, trial,))
            name = cur.fetchone()
        return name
    def get_port_by_event_name_and_trial(self, event, trial):
        with self.conn.cursor() as cur:
            sql = f"SELECT port FROM events , events_to_trials WHERE name=%s AND events_to_trials.trial_name = %s "
            cur.execute(sql, (event, trial,))
            port = cur.fetchone()
        return port

    def get_session_trials(self, sess_id):
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT * FROM session_to_trials WHERE session_id={sess_id}')
            trials = cur.fetchall()
        return trials

    def get_all_session_trials(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM session_to_trials")
            trials = cur.fetchall()
        return trials

    def get_trial_types(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM trials")
            trials_types = cur.fetchall()
        return trials_types

    def get_sessions_names(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT name FROM sessions")
            sessions_names = cur.fetchall()
        return sessions_names

    def get_ports(self, trial_name):
        with self.conn.cursor() as cur:
            temp = f"SELECT port, type, name FROM events, events_to_trials WHERE name = event_name AND " \
                   f"trial_name = '{trial_name}'"
            cur.execute(temp)
            ports = cur.fetchall()
        return ports

    def get_used_ports(self):
        with self.conn.cursor() as cur:
            temp = f"SELECT port FROM events"
            cur.execute(temp)
            ports = cur.fetchall()
        return ports

    def get_dependencies(self, trial_name):
        with self.conn.cursor() as cur:
            temp = f"SELECT h1.port, h2.port FROM events as h1, events as h2, events_to_trials WHERE h1.name = " \
                   f"event_name AND h2.name = contingent_on AND contingent_on IS NOT NULL AND trial_name = '{trial_name}'"
            cur.execute(temp)
            dependencies = cur.fetchall()
        return dependencies

    def get_trial_names(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT name FROM trials")
            trials_types = cur.fetchall()
        return trials_types

    def get_trial_types_names(self, name):
        with self.conn.cursor() as cur:
            temp = f"SELECT name FROM trials WHERE name = '{name}'"
            cur.execute(temp)
            trials_types_names = cur.fetchone()
        return trials_types_names

    def get_trial_name_by_events(self, events):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT name FROM trials WHERE events = '{events}'")
            trials_types_events = cur.fetchone()
        return trials_types_events

    def get_trial_name_by_session(self, session_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT trial_name FROM session_to_trials  WHERE session_id = '{session_id}'")
            trials = cur.fetchall()
        return trials

    def get_events_by_trial_name(self, trial):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT event_name FROM events_to_trials WHERE trial_name = '{trial}'")
            events = cur.fetchall()
        return events
    def get_params_by_event_and_trial_name(self, event, trial,session_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT params FROM session_trial_event_params WHERE event_name = '{event}' AND trial_name='{trial}'AND session_id={session_id}")
            params = cur.fetchall()
        return params

    def get_all_events(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM events")
            events = cur.fetchall()
        return events

    def get_all_sess_for_subject(self, sub_id):
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT * FROM subject_to_session WHERE subject_id={sub_id} ORDER BY last_used')
            sessions = cur.fetchall()
        return sessions

    def update_session_date(self, sess_id):
        with self.conn.cursor() as cur:
            cur.execute(f'UPDATE sessions SET last_used={datetime.date.today()} WHERE session_id={sess_id}')
            self.conn.commit()

    def update_trial_type(self, type_id, name=None, events=None):
        cur = self.conn.cursor()
        if name is not None and events is not None:
            sql = """UPDATE trials SET trial_name=%s, events=%s WHERE type_id=%s"""
            cur.execute(sql, (name, events, type_id,))
        elif name is not None:
            sql = """UPDATE trials SET trial_name=%s WHERE type_id=%s"""
            cur.execute(sql, (name, type_id,))
        else:
            sql = """UPDATE trials SET events=%s WHERE type_id=%s"""
            cur.execute(sql, (events, type_id,))
        self.conn.commit()
        cur.close()

    def delete_trial_type(self, name):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM trials WHERE name = %s", (name,))
            cur.execute(
                "DELETE FROM sessions WHERE NOT EXISTS (SELECT session_id FROM session_to_trials WHERE session_id = sessions.id)")
            self.conn.commit()

    def is_random_event_in_a_given_trial(self, trial, event):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT israndom FROM events_to_trials WHERE event_name='{event}' AND trial_name='{trial}'")
            isRandom = cur.fetchone()
        return isRandom

    def remove_event(self, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT name FROM trials JOIN events_to_trials ON trials.name = trial_name AND event_name = %s ",
                (name,))
            a = cur.fetchall()
            for trial in a:
                t = trial[0]
                self.delete_trial_type(t)
            cur.execute("DELETE FROM events WHERE name =  %s ", (name,))
            cur.execute(
                "DELETE FROM sessions WHERE NOT EXISTS (SELECT session_id FROM session_to_trials WHERE session_id = sessions.id)")
            self.conn.commit()

    def get_iti_vals(self, session_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT min_iti , max_iti FROM sessions WHERE id={session_id}")
            vals = cur.fetchone()
        return vals

    def get_max_trial_time(self, session_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT max_trial_time FROM sessions WHERE id={session_id}")
            max_trial_time = cur.fetchone()
        return max_trial_time

    def delete_subject_session(self, sub_id, sess_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM subjectSession WHERE session_id=%s, subject_id=%s", (sess_id, sub_id))
            self.conn.commit()

    def get_subjects(self):
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT subjectid FROM sessions')
            subjects = cur.fetchall()
        return subjects

    def is_contingent(self, event, trial):
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT is_contingent FROM events_to_trials WHERE event_name='{event}' AND trial_name='{trial}'")
            isContingent = cur.fetchone()
        return isContingent

    def get_sessions_by_subject(self, subject):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT id,name FROM sessions WHERE subjectid='{subject}'")
            sessions = cur.fetchall()
        return sessions

    def is_input_event(self, name):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT type FROM events WHERE name='{name}' AND type='Input'")
            isInput = cur.fetchone()
        return isInput is not None
    def insert_params(self, trial_name, event_name, params,session_id):
        sql = """INSERT INTO session_trial_event_params (session_id, trial_name,event_name ,params) VALUES (%s,%s,%s,%s)"""
        with self.conn.cursor() as cur:
            cur.execute(sql, (session_id, trial_name,event_name ,params))
            self.conn.commit()

    def get_template(self, session_id, subject):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM sessions WHERE id='{session_id}' AND subjectid='{subject}'")
            template = cur.fetchall()
            return template

    def isReward(self, event):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT is_reward FROM events WHERE name = '{event}'")
            isreward = cur.fetchone()
        return isreward


commands = (
    """CREATE TABLE IF NOT EXISTS public.events (
        port VARCHAR(50),
        name VARCHAR(100) UNIQUE,
        type VARCHAR(10),
        format VARCHAR(10),
        is_reward BOOLEAN DEFAULT false,
        CONSTRAINT type_ck CHECK (type in ('Input', 'Output')),
        CONSTRAINT format_ck CHECK (format in ('Analog', 'Digital')))""",

    """CREATE TABLE IF NOT EXISTS public.trials (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE ) """,

    """CREATE TABLE IF NOT EXISTS public.sessions(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) ,
        subjectID VARCHAR(100),
        experimenter_name VARCHAR(100),
        last_used DATE NOT NULL,
        min_iti DOUBLE PRECISION ,
        max_iti DOUBLE PRECISION ,
        is_fixed_iti BOOLEAN DEFAULT false,
        max_trial_time DOUBLE PRECISION,
        notes VARCHAR(2000)
        )""",

    """CREATE TABLE IF NOT EXISTS public.events_to_trials (
        id SERIAL PRIMARY KEY,
        event_name VARCHAR(100) REFERENCES events(name) ON DELETE CASCADE ,
        trial_name VARCHAR(255) REFERENCES trials(name) ON DELETE CASCADE,
        is_contingent BOOLEAN DEFAULT false,
        contingent_on VARCHAR(100),
        isRandom BOOLEAN,
        isEndCondition BOOLEAN,
        preCondition VARCHAR(255))""",

    """CREATE TABLE IF NOT EXISTS public.session_to_trials(
        id SERIAL PRIMARY KEY,
        session_id INTEGER REFERENCES sessions(id),
        trial_name VARCHAR(255) REFERENCES trials(name) ON DELETE CASCADE)""",

    """CREATE TABLE IF NOT EXISTS public.session_trial_event_params(
        id SERIAL PRIMARY KEY,
        session_id INTEGER REFERENCES sessions(id),
        trial_name VARCHAR(255) REFERENCES trials(name) ON DELETE CASCADE,
        event_name VARCHAR(255) REFERENCES events(name) ON DELETE CASCADE,
        params VARCHAR (255))""",


)
