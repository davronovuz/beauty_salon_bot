from datetime import datetime
from .database import Database

class BeautySalonDatabase(Database):
    def __init__(self, path_to_db="beauty_salon.db"):
        super().__init__(path_to_db)

    def create_tables(self):
        # Users table
        sql_users = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id VARCHAR(50) UNIQUE NOT NULL,
            username VARCHAR(50) NULL,
            full_name VARCHAR(100) NULL,
            phone_number VARCHAR(15) NULL,
            language VARCHAR(10) NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            is_blocked BOOLEAN DEFAULT FALSE
        );
        """
        self.execute(sql_users, commit=True)

        # Barbers table
        sql_barbers = """
        CREATE TABLE IF NOT EXISTS barbers (
            barber_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(15) UNIQUE,
            work_schedule TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(sql_barbers, commit=True)

        # Bookings table
        sql_bookings = """
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            barber_id INTEGER NOT NULL,
            booking_date DATE NOT NULL,
            booking_time TIME NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (barber_id, booking_date, booking_time),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (barber_id) REFERENCES barbers(barber_id)
        );
        """
        self.execute(sql_bookings, commit=True)

        # Services table
        sql_services = """
        CREATE TABLE IF NOT EXISTS services (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            duration TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(sql_services, commit=True)

        # Barber Services table
        sql_barber_services = """
        CREATE TABLE IF NOT EXISTS barber_services (
            barber_service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            barber_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (barber_id) REFERENCES barbers(barber_id),
            FOREIGN KEY (service_id) REFERENCES services(service_id)
        );
        """
        self.execute(sql_barber_services, commit=True)

        # Admins table
        sql_admins = """
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name VARCHAR(100) NOT NULL,
            is_super_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """
        self.execute(sql_admins, commit=True)

        # Cancellations table
        sql_cancellations = """
        CREATE TABLE IF NOT EXISTS cancellations (
            cancellation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
        );
        """
        self.execute(sql_cancellations, commit=True)

        # Feedback table
        sql_feedback = """
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            booking_id INTEGER NOT NULL,
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
        );
        """
        self.execute(sql_feedback, commit=True)

        # Working Hours table
        sql_working_hours = """
        CREATE TABLE IF NOT EXISTS working_hours (
            working_hour_id INTEGER PRIMARY KEY AUTOINCREMENT,
            barber_id INTEGER NOT NULL,
            day_of_week VARCHAR(15) NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            break_start TIME,
            break_end TIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (barber_id) REFERENCES barbers(barber_id)
        );
        """
        self.execute(sql_working_hours, commit=True)

    # Add other CRUD operations as needed for beauty salon operations

    def add_user(self, telegram_id, username:None, full_name:None, phone_number:None, language:None):
        sql = """
        INSERT INTO users (telegram_id, username, full_name, phone_number, language, created_at) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        parameters = (telegram_id, username, full_name, phone_number, language, datetime.now())
        self.execute(sql, parameters, commit=True)

    def add_booking(self, user_id, barber_id, booking_date, booking_time, status='pending'):
        sql = """
        INSERT INTO bookings (user_id, barber_id, booking_date, booking_time, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        parameters = (user_id, barber_id, booking_date, booking_time, status, datetime.now())
        self.execute(sql, parameters, commit=True)

    def add_service(self, service_name, description, price, duration):
        sql = """
        INSERT INTO services (service_name, description, price, duration, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        parameters = (service_name, description, price, duration, datetime.now())
        self.execute(sql, parameters, commit=True)

    def link_barber_service(self, barber_id, service_id):
        sql = "INSERT INTO barber_services (barber_id, service_id, created_at) VALUES (?, ?, ?)"
        parameters = (barber_id, service_id, datetime.now())
        self.execute(sql, parameters, commit=True)

    def get_user(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id = ?"
        return self.execute(sql, (telegram_id,), fetchone=True)

    def get_all_users(self):
        sql = "SELECT * FROM users"
        return self.execute(sql, fetchall=True)

    def update_user_phone(self, user_id, new_phone_number):
        sql = "UPDATE users SET phone_number = ? WHERE user_id = ?"
        parameters = (new_phone_number, user_id)
        self.execute(sql, parameters, commit=True)

    def deactivate_user(self, user_id):
        sql = "UPDATE users SET is_active = FALSE WHERE user_id = ?"
        self.execute(sql, (user_id,), commit=True)

    def activate_user(self, user_id):
        sql = "UPDATE users SET is_active = TRUE WHERE user_id = ?"
        self.execute(sql, (user_id,), commit=True)

    def mark_user_as_blocked(self, user_id):
        sql = "UPDATE users SET is_blocked = TRUE, is_active = FALSE WHERE user_id = ?"
        self.execute(sql, (user_id,), commit=True)

    def add_admin(self, user_id, name, is_super_admin=False):
        sql = "INSERT INTO admins (user_id, name, is_super_admin, created_at) VALUES (?, ?, ?, ?)"
        parameters = (user_id, name, is_super_admin, datetime.now())
        self.execute(sql, parameters, commit=True)

    def get_admins(self):
        sql = "SELECT * FROM admins"
        return self.execute(sql, fetchall=True)

    def remove_admin(self, admin_id):
        sql = "DELETE FROM admins WHERE admin_id = ?"
        self.execute(sql, (admin_id,), commit=True)

    def add_feedback(self, user_id, booking_id, rating, comments):
        sql = """
        INSERT INTO feedback (user_id, booking_id, rating, comments, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        parameters = (user_id, booking_id, rating, comments, datetime.now())
        self.execute(sql, parameters, commit=True)

    def get_feedback_for_booking(self, booking_id):
        sql = "SELECT * FROM feedback WHERE booking_id = ?"
        return self.execute(sql, (booking_id,), fetchall=True)

    def cancel_booking(self, booking_id, reason):
        sql_update = "UPDATE bookings SET status = 'cancelled' WHERE booking_id = ?"
        self.execute(sql_update, (booking_id,), commit=True)
        sql_insert = """
        INSERT INTO cancellations (booking_id, reason, created_at)
        VALUES (?, ?, ?)
        """
        parameters = (booking_id, reason, datetime.now())
        self.execute(sql_insert, parameters, commit=True)

    def get_bookings_by_user(self, user_id):
        sql = "SELECT * FROM bookings WHERE user_id = ?"
        return self.execute(sql, (user_id,), fetchall=True)

    def get_bookings_by_barber(self, barber_id):
        sql = "SELECT * FROM bookings WHERE barber_id = ?"
        return self.execute(sql, (barber_id,), fetchall=True)

    def get_available_times(self, barber_id, booking_date):
        sql = """
        SELECT working_hours.start_time, working_hours.end_time
        FROM working_hours
        WHERE barber_id = ? AND day_of_week = strftime('%w', ?)
        """
        return self.execute(sql, (barber_id, booking_date), fetchall=True)

    def update_booking_status(self, booking_id, status):
        sql = "UPDATE bookings SET status = ? WHERE booking_id = ?"
        self.execute(sql, (status, booking_id), commit=True)
