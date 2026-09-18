import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import pyodbc
from datetime import datetime
import threading
import os
from pathlib import Path

class DefectImporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Defect Data Importer - SQL Server")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.excel_file = tk.StringVar()
        self.server_name = tk.StringVar(value="localhost")
        self.database_name = tk.StringVar(value="DefectDatabase")
        self.auth_type = tk.StringVar(value="Windows")
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Defect Data Importer", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Excel File Selection
        ttk.Label(main_frame, text="Excel File:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.excel_file, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=1, column=2, padx=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # SQL Server Configuration
        config_label = ttk.Label(main_frame, text="SQL Server Configuration", font=("Arial", 11, "bold"))
        config_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Server Name
        ttk.Label(main_frame, text="Server Name:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.server_name, width=40).grid(row=4, column=1, columnspan=2, padx=5)
        
        # Database Name
        ttk.Label(main_frame, text="Database Name:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.database_name, width=40).grid(row=5, column=1, columnspan=2, padx=5)
        
        # Authentication Type
        ttk.Label(main_frame, text="Authentication:").grid(row=6, column=0, sticky=tk.W, pady=5)
        auth_frame = ttk.Frame(main_frame)
        auth_frame.grid(row=6, column=1, columnspan=2, sticky=tk.W, padx=5)
        ttk.Radiobutton(auth_frame, text="Windows", variable=self.auth_type, value="Windows").pack(anchor=tk.W)
        ttk.Radiobutton(auth_frame, text="SQL Server", variable=self.auth_type, value="SQLServer").pack(anchor=tk.W)
        
        # Credentials frame (initially hidden)
        self.creds_frame = ttk.LabelFrame(main_frame, text="SQL Server Credentials")
        self.creds_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        ttk.Label(self.creds_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(self.creds_frame, textvariable=self.username, width=35).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.creds_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(self.creds_frame, textvariable=self.password, width=35, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        self.creds_frame.grid_remove()
        
        self.auth_type.trace('w', self.toggle_credentials)
        
        # Progress section
        progress_label = ttk.Label(main_frame, text="Import Progress", font=("Arial", 11, "bold"))
        progress_label.grid(row=8, column=0, columnspan=3, sticky=tk.W, pady=(15, 5))
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Status text
        self.status_text = tk.Text(main_frame, height=6, width=70, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.grid(row=10, column=0, columnspan=3, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.status_text.yview)
        scrollbar.grid(row=10, column=3, sticky=(tk.N, tk.S), padx=(0, 5), pady=5)
        self.status_text['yscrollcommand'] = scrollbar.set
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=3, pady=15, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="Import Data", command=self.start_import).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def toggle_credentials(self, *args):
        """Show/hide credentials based on authentication type"""
        if self.auth_type.get() == "SQLServer":
            self.creds_frame.grid()
        else:
            self.creds_frame.grid_remove()
    
    def browse_file(self):
        """Browse for Excel file"""
        filename = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.excel_file.set(filename)
            self.log_message(f"Selected file: {filename}")
    
    def log_message(self, message):
        """Add message to status log"""
        self.status_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_log(self):
        """Clear the log"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def start_import(self):
        """Start the import process in a separate thread"""
        if not self.excel_file.get():
            messagebox.showerror("Error", "Please select an Excel file")
            return
        
        # Disable button and start progress bar
        self.progress.start()
        thread = threading.Thread(target=self.import_data, daemon=True)
        thread.start()
    
    def import_data(self):
        """Import data to SQL Server"""
        try:
            self.log_message("Starting import process...")
            
            # Read Excel file
            self.log_message(f"Reading Excel file: {self.excel_file.get()}")
            df = pd.read_excel(self.excel_file.get(), sheet_name='Sheet1')
            self.log_message(f"✓ Loaded {len(df)} defect records")
            
            # Build connection string
            server = self.server_name.get()
            database = self.database_name.get()
            
            if self.auth_type.get() == "Windows":
                conn_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server};Database=master;Trusted_Connection=yes;"
                self.log_message("Using Windows Authentication")
            else:
                username = self.username.get()
                password = self.password.get()
                if not username or not password:
                    self.log_message("✗ Error: Please provide username and password")
                    self.progress.stop()
                    return
                conn_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database=master;UID={username};PWD={password};"
                self.log_message("Using SQL Server Authentication")
            
            # Connect to master database to create new database
            self.log_message("Connecting to SQL Server...")
            conn = pyodbc.connect(conn_string, autocommit=True)
            cursor = conn.cursor()
            self.log_message("✓ Connected to SQL Server")
            
            # Create database if it doesn't exist
            self.log_message(f"Creating database '{database}' if it doesn't exist...")
            cursor.execute(f"IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = N'{database}') CREATE DATABASE {database}")
            self.log_message(f"✓ Database '{database}' ready")
            
            cursor.close()
            conn.close()
            
            # Connect to the new database
            if self.auth_type.get() == "Windows":
                conn_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};Trusted_Connection=yes;"
            else:
                conn_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};UID={username};PWD={password};"
            
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
            
            # Create table
            self.log_message("Creating 'Defects' table...")
            create_table_sql = """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'Defects')
            CREATE TABLE Defects (
                DefectID INT PRIMARY KEY IDENTITY(1,1),
                Project NVARCHAR(50),
                Trace_Defect NVARCHAR(MAX),
                MES_Failure NVARCHAR(MAX),
                MES_Location NVARCHAR(MAX),
                MES_Fail_Category NVARCHAR(100),
                MES_DDS_Category NVARCHAR(100),
                Stages NVARCHAR(100),
                ImportedDate DATETIME DEFAULT GETDATE()
            )
            """
            cursor.execute(create_table_sql)
            conn.commit()
            self.log_message("✓ Table created")
            
            # Insert data
            self.log_message("Inserting defect records...")
            insert_sql = """
            INSERT INTO Defects (Project, Trace_Defect, MES_Failure, MES_Location, MES_Fail_Category, MES_DDS_Category, Stages)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            for idx, row in df.iterrows():
                try:
                    cursor.execute(insert_sql, (
                        str(row['Project']) if pd.notna(row['Project']) else None,
                        str(row['Trace_Defect']) if pd.notna(row['Trace_Defect']) else None,
                        str(row['MES_Failure']) if pd.notna(row['MES_Failure']) else None,
                        str(row['MES_Location']) if pd.notna(row['MES_Location']) else None,
                        str(row['MES_Fail_Category']) if pd.notna(row['MES_Fail_Category']) else None,
                        str(row['MES_DDS_Category']) if pd.notna(row['MES_DDS_Category']) else None,
                        str(row['Stages']) if pd.notna(row['Stages']) else None,
                    ))
                    if (idx + 1) % 100 == 0:
                        conn.commit()
                        self.log_message(f"✓ Inserted {idx + 1} records...")
                except Exception as e:
                    self.log_message(f"✗ Error inserting row {idx + 1}: {str(e)}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            self.log_message(f"✓ All {len(df)} defect records imported successfully!")
            self.log_message(f"Database: {server}\\{database}")
            messagebox.showinfo("Success", f"Successfully imported {len(df)} defect records!\n\nDatabase: {database}\nServer: {server}")
            
        except pyodbc.Error as e:
            self.log_message(f"✗ SQL Server Error: {str(e)}")
            messagebox.showerror("SQL Server Error", f"Database Error:\n{str(e)}")
        except FileNotFoundError:
            self.log_message(f"✗ File not found: {self.excel_file.get()}")
            messagebox.showerror("Error", "Excel file not found")
        except Exception as e:
            self.log_message(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.progress.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DefectImporterApp(root)
    root.mainloop()
