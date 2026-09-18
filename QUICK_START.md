# Quick Start Guide - Defect Importer

## 🚀 Fast Setup (5 minutes)

### Step 1: Prepare
- Ensure SQL Server is running
- Know your SQL Server name (e.g., `localhost`, `LAPTOP-XYZ`, or `.\SQLEXPRESS`)

### Step 2: Build the EXE
**Windows Command Prompt:**
```
build_exe.bat
```

**Windows PowerShell:**
```
.\build_exe.ps1
```

### Step 3: Run
Double-click: `dist\Defect_Importer.exe`

## Usage in 3 Steps

1. **Click "Browse"** → Select your Excel file
2. **Enter Server Name** → (e.g., `localhost` or your server name)
3. **Click "Import Data"** → Wait for success message

## Common Server Names

| Environment | Server Name |
|-------------|-------------|
| Local (Default) | `localhost` |
| Local (Shorthand) | `.` |
| SQL Server Express | `.\SQLEXPRESS` |
| Named Instance | `COMPUTERNAME\INSTANCENAME` |
| Remote Server | `SERVER_IP_ADDRESS` |

## Need Help?

- **Won't connect?** Check if SQL Server is running: `Start → Services → SQL Server`
- **Driver missing?** Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- **More details?** See README.md

---

**That's it!** Your defect data is now in SQL Server. 🎉
