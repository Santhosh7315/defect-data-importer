# Troubleshooting Guide

## Common Issues & Solutions

### 1. "Cannot Connect to Server" or "Connection refused"

**Symptoms:** Error message when clicking Import Data

**Possible Causes:**
- SQL Server is not running
- Wrong server name
- Network/firewall issues
- SQL Server TCP/IP is disabled

**Solutions:**

a) **Check if SQL Server is running:**
   - Windows + R
   - Type: `services.msc`
   - Look for "SQL Server (MQLSERVER)" or "SQL Server Express"
   - Should show "Running" status
   - If not running, right-click → Start

b) **Verify correct server name:**
   - Open SQL Server Management Studio (SSMS)
   - Check server name at top
   - Copy exact name to Defect Importer

c) **Try alternative server names:**
   - `localhost` (local default instance)
   - `.` (shorthand for localhost)
   - `127.0.0.1` (IP address)
   - `COMPUTERNAME\SQLEXPRESS` (if using Express)

d) **Enable TCP/IP (if local SQL Server):**
   - Windows + R → `SQLServerManager15.msc`
   - SQL Server Network Configuration → TCP/IP
   - Right-click TCP/IP → Enable
   - Restart SQL Server service

---

### 2. "Login failed" or "Authentication Error"

**Symptoms:** Error when using SQL Server authentication

**Possible Causes:**
- Wrong username/password
- SQL Server user doesn't exist
- User account disabled
- Insufficient permissions

**Solutions:**

a) **Verify credentials in SSMS:**
   - Open SQL Server Management Studio
   - Try logging in with same username/password
   - If it fails in SSMS, credentials are wrong

b) **Create new SQL Server user (if admin):**
   - In SSMS, expand Security → Logins
   - Right-click → New Login
   - Create new user with password
   - Right-click user → Properties → Server Roles
   - Check "sysadmin" role
   - Click OK

c) **Use Windows Authentication instead:**
   - Easier and more secure
   - Select "Windows" in Defect Importer
   - No password needed

d) **Reset SQL Server sa password (if admin):**
   - Right-click SQL Server instance → Properties
   - Click "Security" tab
   - Restart SQL Server in mixed mode (if needed)

---

### 3. "ODBC Driver 17 not found"

**Symptoms:** "Driver={ODBC Driver 17 for SQL Server} not found"

**Possible Causes:**
- ODBC Driver 17 not installed
- ODBC Driver for different version installed

**Solutions:**

a) **Install ODBC Driver 17:**
   - Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Run installer as Administrator
   - Choose "Repair" if already installed
   - Restart computer

b) **If different version installed:**
   - Control Panel → Programs → Programs and Features
   - Look for "Microsoft ODBC Driver..."
   - Uninstall it
   - Install ODBC Driver 17

c) **Verify installation:**
   - Windows + R
   - Type: `odbcad32.exe`
   - Look for "ODBC Driver 17 for SQL Server" in Drivers tab

---

### 4. "File not found" or Excel file error

**Symptoms:** Error when trying to open Excel file

**Possible Causes:**
- Wrong file path
- File doesn't exist
- File is open in another program
- Wrong file format

**Solutions:**

a) **Check file exists:**
   - Browse using "Browse" button instead of typing path
   - Verify file path is correct

b) **Close Excel file:**
   - If file is open in Excel, close it first
   - Excel locks files while open

c) **Verify file format:**
   - File should be .xlsx or .xls
   - Ensure it has "Sheet1" tab
   - Open file in Excel to verify data

d) **Try different path formats:**
   - Avoid special characters in filename
   - Use full path: `C:\Users\YourName\Desktop\file.xlsx`
   - Avoid network paths if possible

---

### 5. "Database already exists" error

**Symptoms:** Cannot create new database

**Possible Causes:**
- Database with same name already exists
- Insufficient permissions

**Solutions:**

a) **Use different database name:**
   - Change "Database Name" field
   - Example: "DefectDatabase_v2"
   - Click Import Data again

b) **Delete existing database (if safe):**
   - In SSMS, right-click database → Delete
   - Select "Close existing connections"
   - Click OK

c) **Check permissions:**
   - Ensure user has "Create Database" permission
   - May need to use admin account

---

### 6. "Import stalled" or "hangs"

**Symptoms:** Progress bar running but nothing happening

**Possible Causes:**
- Large file taking time
- Network issues
- SQL Server performance

**Solutions:**

a) **Wait longer:**
   - Large files (600+ records) take time
   - Give it 2-5 minutes per 1000 records

b) **Close other applications:**
   - Frees up system resources
   - Closes other database connections

c) **Check SQL Server:**
   - Open SSMS
   - Check if SQL Server is responding
   - Restart if needed

d) **Reduce file size:**
   - Split Excel file into smaller chunks
   - Import separately

---

### 7. "Permission denied" or "Access denied"

**Symptoms:** Cannot create database or table

**Possible Causes:**
- User lacks permissions
- Using non-admin account

**Solutions:**

a) **Run as Administrator:**
   - Right-click Defect_Importer.exe
   - Click "Run as administrator"

b) **Grant permissions to user:**
   - Use admin account in SSMS
   - Right-click user login → Properties
   - Grant "Create Database" in Server Roles
   - Grant "db_owner" role in database

c) **Use sa account:**
   - sa is system admin with full permissions
   - Use sa username with password

---

### 8. Build fails with "PyInstaller not found"

**Symptoms:** Error when running build_exe.bat

**Possible Causes:**
- Python not installed
- Python not in PATH
- pip installation failed

**Solutions:**

a) **Verify Python installation:**
   - Windows + R
   - Type: `python --version`
   - Should show version number
   - If not, install Python from https://www.python.org/

b) **Add Python to PATH:**
   - During Python installation, check "Add Python to PATH"
   - Or manually add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311`

c) **Install pip:**
   ```
   python -m pip install --upgrade pip
   ```

d) **Rebuild:**
   ```
   build_exe.bat
   ```

---

### 9. EXE runs but shows "No module named..."

**Symptoms:** EXE launches then error about missing module

**Possible Causes:**
- Python dependencies not installed
- Build process incomplete

**Solutions:**

a) **Reinstall dependencies:**
   ```
   pip install -r requirements.txt
   ```

b) **Rebuild EXE:**
   ```
   build_exe.bat
   ```

c) **Delete build files:**
   - Delete `build` and `dist` folders
   - Rebuild fresh

---

### 10. Import completes but data not in database

**Symptoms:** Success message but no data in SQL Server

**Possible Causes:**
- Data inserted to wrong database
- Table not created properly
- Wrong server connection

**Solutions:**

a) **Verify in SSMS:**
   - Open SQL Server Management Studio
   - Check correct database selected
   - Right-click → New Query
   - Run: `SELECT COUNT(*) FROM Defects;`

b) **Check table exists:**
   ```sql
   SELECT * FROM INFORMATION_SCHEMA.TABLES;
   ```

c) **Check database:**
   ```sql
   SELECT name FROM sys.databases;
   ```

d) **Reimport to different database name:**
   - Change database name and try again

---

## Getting Help

If you still have issues:

1. **Check the log window:**
   - Scroll through the import progress log
   - Look for specific error messages

2. **Google the error:**
   - Copy exact error message
   - Search it online

3. **Check SQL Server logs:**
   - SQL Server Management Studio
   - Management → SQL Server Logs
   - Review latest entries

4. **Collect information:**
   - SQL Server version
   - Windows version
   - Exact error message
   - Python version (if running from source)

---

## Advanced Diagnostics

### Test SQL Server connectivity:

```batch
REM Test connectivity
sqlcmd -S localhost -E

REM Should show: 1>
REM If it works, you can connect
```

### Check ODBC drivers:

```batch
REM List ODBC drivers
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBCINST.INI"
```

### View Python details:

```batch
python --version
pip --version
pip show pyodbc
pip show pandas
```

---

## Still Stuck?

- Review the main README.md
- Check QUICK_START.md for basic setup
- Review the application log messages
- Verify prerequisites are installed
- Ensure SQL Server is accessible

Good luck! 🚀
