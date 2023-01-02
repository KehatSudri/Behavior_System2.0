import datetime
import logging
import sys

import psycopg2
from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def config(filename):
    section = 'postgresql'
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section "postgresql" not found in file'.format(section, filename))

    return db


class DB:
    def __init__(self, filename):
        self.conn = None
        db_config = config(filename)
        temp = db_config['database']
        db_config['database'] = 'postgres'
        self.connect(db_config)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.create_db()
        db_config['database'] = temp
        self.disconnect()
        self.connect(db_config)
        self.create_tables()

    def connect(self, params):
        """ Connect to the PostgreSQL database server """
        try:
            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f'{error}')
            sys.exit()

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'Behavior_sys'")
            exists = cur.fetchone()
            print(exists)
            if exists is None:
                cur.execute('CREATE DATABASE "Behavior_sys"')
            else:
                pass

    def create_tables(self):
        with self.conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
            self.conn.commit()

    def insert_hardware_event(self, name, port, in_out, digital_analog, is_reward):
        sql = """
            INSERT INTO hardwareEvents(event_name,port,input_output ,digital_analog,is_reward) VALUES (%s,%s,%s,%s,%s)
             ON CONFLICT (event_name) DO UPDATE SET port=%s,input_output=%s ,digital_analog=%s,is_reward=%s RETURNING event_id"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql,
                            (name, port, in_out, digital_analog, is_reward, port, in_out, digital_analog, is_reward,))
                e_id = cur.fetchone()[0]
                self.conn.commit()
            return e_id
        except Exception:
            return -1

    def insert_session(self, iti_type, end_def, end_val, trials_order, iti_min_range=None, iti_max_range=None,
                       iti_behave_def=None, total_num=None, block_size=None, blocks_ord=None, sess_name=None,
                       exp_name=None, rnd_rew_percent=None):
        sql = """
            INSERT INTO sessions(session_name,experimenter_name,iti_type,iti_min_range,iti_max_range,iti_behave_definition,
            end_definition,end_value,trials_order,total_trials,block_size,blocks_order, random_reward_percent,last_used)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
             RETURNING session_id"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql,
                            (sess_name, exp_name, iti_type, iti_min_range, iti_max_range, iti_behave_def, end_def,
                             end_val,
                             trials_order, total_num,
                             str(block_size), str(blocks_ord), rnd_rew_percent, datetime.date.today()))
                sess_id = cur.fetchone()[0]
                self.conn.commit()
            return sess_id
        except Exception:
            return -1

    def insert_trial_type(self, name, events=None):
        sql = """INSERT INTO trialTypes(trial_name ,events) VALUES (%s,%s)"""
        cur = self.conn.cursor()
        cur.execute(sql, (name, events,))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        self.conn.commit()

    def insert_session_trials(self, session_id, trial_type_id, percent_in_session=None,
                              percent_in_block=None, block_number=None, event_list=None, interval_list=None):
        sql = """INSERT INTO sessionTrials(session_id, trial_type_id, percent_in_session,percent_in_block, block_number,
                              event_list,interval_list) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING session_trial_id"""
        cur = self.conn.cursor()
        # cur.execute(sql, ("A15B6", "behaviour", None, None, 15, 20, "time"))
        cur.execute(sql, (
            session_id, trial_type_id, percent_in_session, percent_in_block, block_number, event_list, interval_list))
        # session_id, trial_type_id, percent_in_session, percent_in_block, block_number, event_list, interval_list))
        sess_trial_id = cur.fetchone()[0]
        # sess_id = cur.fetchone()[0]
        self.conn.commit()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        self.conn.commit()
        return sess_trial_id

    def insert_event(self, event_type, parameters=None):
        sql = """INSERT INTO events(event_type, parameters) VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING event_id"""
        cur = self.conn.cursor()
        cur.execute(sql, (event_type, parameters))
        fetch = cur.fetchone()
        # event_id = cur.fetchone()[0]
        event_id = None
        if cur.statusmessage != "INSERT 0 0":
            event_id = fetch[0]
            self.conn.commit()
        else:
            sql = """SELECT event_id FROM events WHERE event_type=%s AND parameters=%s"""
            cur.execute(sql, (event_type, parameters))
            event_id = cur.fetchone()[0]
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        self.conn.commit()
        return event_id

    def insert_subject_session(self, subject_id, session_id, counter=0):
        # on conflict increment counter by 1, and last used is now
        sql = """INSERT INTO subjectSession(subject_id, session_id, counter,last_used) VALUES (%s,%s,%s,%s) 
                ON CONFLICT ON CONSTRAINT sbjsess_pkey DO UPDATE SET last_used=%s"""
        cur = self.conn.cursor()
        # cur.execute(sql, ("A15B6", "behaviour", None, None, 15, 20, "time"))
        cur.execute(sql, (subject_id, session_id, counter, datetime.date.today(), datetime.date.today()))
        self.conn.commit()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        self.conn.commit()
        return

    def get_session_templates(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM sessions")
            sessions = cur.fetchall()
        return sessions

    def get_hardware_events(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM hardwareEvents")
            events = cur.fetchall()
        return events

    def get_session_trials(self, sess_id):
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT * FROM sessionTrials WHERE session_id={sess_id}')
            trials = cur.fetchall()
        return trials

    def get_all_session_trials(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM sessionTrials")
            trials = cur.fetchall()
        return trials

    def get_trial_types(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM trialTypes")
            trials_types = cur.fetchall()
        return trials_types

    def get_trial_types_names(self, name):
        with self.conn.cursor() as cur:
            temp = f"SELECT trial_name FROM trialTypes WHERE trial_name = '{name}'"
            cur.execute(temp)
            trials_types_names = cur.fetchone()
        return trials_types_names

    def get_trial_name_by_events(self, events):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT trial_name FROM trialTypes WHERE events = '{events}'")
            trials_types_events = cur.fetchone()
        return trials_types_events

    def get_all_events(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM events")
            events = cur.fetchall()
        return events

    def get_event_by_id(self, event_id):
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT * FROM events WHERE event_id={event_id}')
            events = cur.fetchall()
        return events

    def get_all_subject_sessions(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM subjectSession")
            ans = cur.fetchall()
        return ans

    def get_last_sess_for_subject(self, sub_id):
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT * FROM subjectSession WHERE subject_id={sub_id} ORDER BY last_used')
            session_id = cur.fetchone()
        return session_id

    def get_all_sess_for_subject(self, sub_id):  # TODO validate work
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT * FROM subjectSession WHERE subject_id={sub_id} ORDER BY last_used')
            sessions = cur.fetchall()
        return sessions

    def get_session_by_id(self, sess_id):
        with self.conn.cursor() as cur:
            cur.execute(f'SELECT * FROM sessions WHERE session_id={sess_id}')
            session_id = cur.fetchone()
        return session_id

    def update_subject_session(self, sub_id, sess_id, counter):
        with self.conn.cursor() as cur:
            cur.execute(
                f'UPDATE subjectsession SET counter={counter}, last_used={datetime.date.today()} WHERE subject_id={sub_id} AND session_id={sess_id}')
            self.conn.commit()

    def update_session_date(self, sess_id):
        with self.conn.cursor() as cur:
            cur.execute(f'UPDATE sessions SET last_used={datetime.date.today()} WHERE session_id={sess_id}')
            self.conn.commit()

    # TODO validate this functions
    def update_trial_type(self, type_id, name=None, events=None):
        cur = self.conn.cursor()
        if name is not None and events is not None:
            sql = """UPDATE trialTypes SET trial_name=%s, events=%s WHERE type_id=%s"""
            cur.execute(sql, (name, events, type_id,))
        elif name is not None:
            sql = """UPDATE trialTypes SET trial_name=%s WHERE type_id=%s"""
            cur.execute(sql, (name, type_id,))
        else:
            sql = """UPDATE trialTypes SET events=%s WHERE type_id=%s"""
            cur.execute(sql, (events, type_id,))
        self.conn.commit()
        cur.close()

    # TODO validate this functions
    def delete_trial_type(self, type_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(f'DELETE FROM trialTypes WHERE type_id={type_id}')
                self.conn.commit()
            return 0
        except Exception:
            return -1

    # TODO validate this functions
    def delete_template(self, temp_id):
        cur = self.conn.cursor()
        # delete session subjects
        cur.execute("DELETE FROM subjectSession WHERE session_id=%s", (temp_id,))
        # delete session trials
        cur.execute("DELETE FROM sessionTrials WHERE session_id=%s", (temp_id,))
        # delete session
        cur.execute("DELETE FROM sessions WHERE session_id=%s", (temp_id,))
        self.conn.commit()
        cur.close()

    # TODO validate this functions
    def delete_subject_session(self, sub_id, sess_id):
        cur = self.conn.cursor()
        # delete session subjects
        cur.execute("DELETE FROM subjectSession WHERE session_id=%s, subject_id=%s", (sess_id, sub_id))
        self.conn.commit()
        cur.close()

    # TODO delete
    def delete_all_rows(self):
        # on conflict increment counter by 1, and last used is now
        sql = """
        DELETE FROM events
        DELETE FROM sessiontrials
        DELETE FROM subjectsession"""
        cur = self.conn.cursor()
        cur.execute("""DELETE FROM events""")
        cur.execute("""DELETE FROM subjectsession""")
        cur.execute("""DELETE FROM sessiontrials""")
        cur.execute("""DELETE FROM sessions""")

        self.conn.commit()
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        self.conn.commit()


commands = (
    """
    CREATE TABLE IF NOT EXISTS public.hardwareEvents
    (
        event_id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY 
        ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        event_name VARCHAR(250) NOT NULL UNIQUE,
        port VARCHAR(100),
        input_output VARCHAR(20) NOT NULL,
        digital_analog VARCHAR(20) NOT NULL,
        is_reward VARCHAR(20) NOT NULL,       
        CONSTRAINT hardwareEvents_pkey PRIMARY KEY (event_id),
        CONSTRAINT input_output_ck CHECK (input_output in ('Input', 'Output')),
        CONSTRAINT digital_analog_ck CHECK (digital_analog in ('Digital', 'Analog')),
        CONSTRAINT is_reward_ck CHECK (is_reward in ('True', 'False'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS public.sessions
    (
        session_id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY 
        ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        session_name VARCHAR(250),
        experimenter_name VARCHAR(100),
        iti_type VARCHAR(20) NOT NULL,
        iti_min_range integer,
        iti_max_range integer,
        iti_behave_definition VARCHAR(255),
        end_definition VARCHAR(100) NOT NULL,
        end_value integer NOT NULL,
        trials_order VARCHAR(50),
        total_trials integer,
        block_size VARCHAR(100),
        blocks_order VARCHAR(100),
        random_reward_percent integer,
        last_used DATE NOT NULL,               
        CONSTRAINT sessions_pkey PRIMARY KEY (session_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS public.trialTypes (
        type_id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY 
        ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        trial_name VARCHAR(255) UNIQUE,
        events VARCHAR(255) UNIQUE,
        constraint trial_pkey PRIMARY KEY (type_id)
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS public.sessionTrials (
        session_trial_id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY 
        ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        session_id integer REFERENCES sessions,
        trial_type_id integer NOT NULL REFERENCES trialTypes,
        percent_in_session integer,
        percent_in_block VARCHAR(100),
        block_number VARCHAR(100),
        event_list VARCHAR(255),
        interval_list VARCHAR(255),
        constraint sessiontrial_pkey PRIMARY KEY (session_trial_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS public.subjectSession (
        subject_id VARCHAR(100) NOT NULL,
        session_id integer REFERENCES sessions,
        counter integer,
        last_used DATE NOT NULL,
        constraint sbjsess_pkey PRIMARY KEY (subject_id, session_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS public.events (
        event_id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY 
        ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        event_type VARCHAR(100),
        parameters VARCHAR(255),
        constraint eventid_pkey PRIMARY KEY (event_id), 
        constraint type_params_unq UNIQUE (event_type, parameters)
    )
    """
)
