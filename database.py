import sqlite3
import pandas as pd
from datetime import datetime
import bcrypt
import json
import streamlit as st

class Database:
    def __init__(self, db_name="mes_connect.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_database()
    
    def init_database(self):
        # Users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login_id TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'alumni', 'admin')),
            status TEXT DEFAULT 'pending',
            
            date_of_birth TEXT,
            id_card_number TEXT UNIQUE,
            year TEXT CHECK(year IN ('1st Year PUC', '2nd Year PUC')),
            stream TEXT CHECK(stream IN ('Science', 'Commerce', 'Arts')),
            section TEXT,
            graduation_year INTEGER,
            promoted_at DATETIME,
            promoted_by TEXT,
            contact_number TEXT,
            security_question TEXT,
            security_answer TEXT,
            hobbies TEXT,
            current_company TEXT,
            position TEXT,
            linkedin_url TEXT,
            
            profile_image TEXT,
            cover_image TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Connections table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            accepted_at DATETIME,
            FOREIGN KEY (requester_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id),
            UNIQUE(requester_id, receiver_id)
        )
        ''')
        
        # Groups table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            type TEXT DEFAULT 'student',
            category TEXT,
            privacy TEXT DEFAULT 'public',
            created_by INTEGER NOT NULL,
            is_approved BOOLEAN DEFAULT 1,
            member_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        # Group members
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT DEFAULT 'member',
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(group_id, user_id)
        )
        ''')
        
        # Confessions table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS confessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anonymous_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            is_approved BOOLEAN DEFAULT 0,
            is_reported BOOLEAN DEFAULT 0,
            report_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Announcements table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            type TEXT DEFAULT 'general',
            created_by INTEGER NOT NULL,
            attachments TEXT DEFAULT '[]',
            target_roles TEXT DEFAULT '[]',
            is_published BOOLEAN DEFAULT 1,
            views INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        # Create indexes
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_year ON users(year)')
        
        # Insert default admin if not exists
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        if self.cursor.fetchone()[0] == 0:
            hashed_password = self.hash_password("Admin123!@#")
            self.cursor.execute('''
            INSERT INTO users (login_id, email, password, first_name, last_name, role, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin@mes.edu', hashed_password, 'System', 'Admin', 'admin', 'active'))
            self.conn.commit()
    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
    def create_user(self, user_data):
        try:
            hashed_password = self.hash_password(user_data['password'])
            
            query = '''
            INSERT INTO users (login_id, email, password, first_name, last_name, role, 
                              date_of_birth, id_card_number, year, stream, section,
                              contact_number, security_question, security_answer, hobbies, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            values = (
                user_data['login_id'],
                user_data['email'],
                hashed_password,
                user_data['first_name'],
                user_data['last_name'],
                user_data.get('role', 'student'),
                user_data.get('date_of_birth'),
                user_data.get('id_card_number'),
                user_data.get('year'),
                user_data.get('stream'),
                user_data.get('section'),
                user_data.get('contact_number'),
                user_data.get('security_question'),
                user_data.get('security_answer'),
                user_data.get('hobbies'),
                user_data.get('status', 'pending')
            )
            
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
    
    def authenticate_user(self, login_id, password, role):
        try:
            self.cursor.execute('''
            SELECT * FROM users 
            WHERE (login_id = ? OR email = ?) 
            AND role = ? 
            AND status IN ('active', 'pending')
            ''', (login_id, login_id, role))
            
            user = self.cursor.fetchone()
            if user:
                columns = [desc[0] for desc in self.cursor.description]
                user_dict = dict(zip(columns, user))
                
                if self.verify_password(password, user_dict['password']):
                    # Update last login
                    self.cursor.execute(
                        'UPDATE users SET last_login = ? WHERE id = ?',
                        (datetime.now(), user_dict['id'])
                    )
                    self.conn.commit()
                    user_dict.pop('password', None)
                    return user_dict
            return None
        except Exception as e:
            st.error(f"Auth error: {str(e)}")
            return None
    
    def promote_students_to_alumni(self, student_ids, graduation_year, admin_id):
        try:
            placeholders = ','.join(['?'] * len(student_ids))
            query = f'''
            UPDATE users 
            SET role = 'alumni', 
                graduation_year = ?,
                promoted_at = ?,
                promoted_by = ?,
                updated_at = ?
            WHERE id IN ({placeholders}) 
            AND role = 'student'
            '''
            
            values = [graduation_year, datetime.now(), admin_id, datetime.now()] + student_ids
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            st.error(f"Promotion error: {str(e)}")
            return False
    
    def get_students(self):
        self.cursor.execute("SELECT * FROM users WHERE role='student'")
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def get_alumni(self):
        self.cursor.execute("SELECT * FROM users WHERE role='alumni'")
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

db = Database()
