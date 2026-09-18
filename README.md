# Defect Data Importer - SQL Server Edition

A Windows GUI application to import defect data from Excel into SQL Server database.

## Features

✅ **User-Friendly GUI** - Easy-to-use interface  
✅ **SQL Server Integration** - Creates database and table automatically  
✅ **Excel Import** - Reads defect data from Excel files  
✅ **Windows & SQL Authentication** - Flexible authentication options  
✅ **Progress Logging** - Real-time import status updates  
✅ **Error Handling** - Comprehensive error messages  
✅ **Automatic Database Creation** - No manual SQL setup required  

## Prerequisites

### For Running the Python Script
- Python 3.7 or higher
- SQL Server (2016 or later) installed and running
- ODBC Driver 17 for SQL Server (included with SQL Server, can also download separately)

### For Running the EXE
- Windows OS
- SQL Server running on your network
- ODBC Driver 17 for SQL Server

## Installation & Setup

### Option 1: Run as Python Script (Easiest for Testing)

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/
   - During installation, check "Add Python to PATH"

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python defect_importer.py
   ```

### Option 2: Build as EXE (For Distribution)

#### On Windows Command Prompt (CMD):

1. **Open Command Prompt** as Administrator in the folder containing the files

2. **Run the build script**
   ```bash
   build_exe.bat
   ```

3. The script will:
   - Install all required Python packages
   - Install PyInstaller
   - Build the EXE file
   - Place it in `.\dist\Defect_Importer.exe`

#### On Windows PowerShell:

1. **Open PowerShell** as Administrator in the folder containing the files

2. **Allow script execution** (first time only)
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Run the build script**
   ```powershell
   .\build_exe.ps1
   ```

## Usage

### Launching the Application

**As Python Script:**
```bash
python defect_importer.py
```

**As EXE:**
- Double-click `Defect_Importer.exe` in the `dist` folder

### Using the Application

1. **Select Excel File**
   - Click "Browse" and select your defect Excel file
   - The file path will appear in the text field

2. **Configure SQL Server Settings**
   - **Server Name**: Your SQL Server name (e.g., `LAPTOP-ABC123\SQLEXPRESS` or `localhost`)
   - **Database Name**: Name for the new database (default: `DefectDatabase`)
   - **Authentication**: Choose Windows or SQL Server authentication

3. **Set Credentials (if using SQL Server Authentication)**
   - Provide SQL Server username
   - Provide SQL Server password

4. **Click "Import Data"**
   - The progress bar will show the import is running
   - Log messages show real-time status
   - Success message appears when complete

### Finding Your SQL Server Name

**Option A: SQL Server Management Studio**
- Connect to your server
- Server name shown in Object Explorer top bar

**Option B: Command Line**
```bash
sqlcmd -L
```

**Option C: Common defaults**
- `localhost` - Local default instance
- `.\SQLEXPRESS` - SQL Server Express (local)
- `COMPUTERNAME\SQLEXPRESS` - Remote Express

## Database Structure

The application creates a table with the following schema:

```sql
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
```

## Troubleshooting

### Error: "Connection refused" or "Cannot connect to server"

**Solution:**
- Verify SQL Server is running
- Check server name spelling
- Try using `localhost` or `.` for local server
- Enable SQL Server TCP/IP protocol

### Error: "Login failed"

**Solution:**
- Verify username and password if using SQL Server auth
- Use Windows authentication if available
- Check SQL Server user permissions

### Error: "ODBC Driver 17 not found"

**Solution:**
- Install ODBC Driver 17 for SQL Server from:
  https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### Error: "File not found"

**Solution:**
- Verify the Excel file path is correct
- Ensure file is not open in another application
- Use absolute paths if possible

### Application won't start after building EXE

**Solution:**
- Rebuild the EXE: `build_exe.bat`
- Ensure Python is still installed
- Delete the `build` and `dist` folders and rebuild

## File Descriptions

| File | Purpose |
|------|---------|
| `defect_importer.py` | Main application source code |
| `requirements.txt` | Python package dependencies |
| `build_exe.bat` | Batch script to build EXE (Windows CMD) |
| `build_exe.ps1` | PowerShell script to build EXE |
| `README.md` | This documentation |

## Advanced Options

### Customize the Build

Edit `build_exe.bat` or `build_exe.ps1` to customize:
- Change `--name "Defect_Importer"` to different name
- Add `--icon=your_icon.ico` for custom icon
- Add `--onedir` instead of `--onefile` for smaller file size

### Run as Scheduled Task

To run imports automatically:

1. Build the EXE
2. Create a batch file:
   ```batch
   @echo off
   cd C:\path\to\your\files
   Defect_Importer.exe
   ```
3. Use Task Scheduler to run this batch file on a schedule

## Support

For issues:
1. Check error messages in the log window
2. Review the Troubleshooting section
3. Verify all prerequisites are installed
4. Check SQL Server is running and accessible

## License

This application is provided as-is for your use.

## Version Info

- **Version**: 1.0
- **Python Version**: 3.7+
- **SQL Server**: 2016 or later
- **Built**: 2026
