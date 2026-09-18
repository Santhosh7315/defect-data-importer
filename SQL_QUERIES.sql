-- Defect Data Importer - SQL Query Reference
-- Use these queries in SQL Server Management Studio to analyze your defect data

-- ============================================
-- BASIC QUERIES
-- ============================================

-- 1. View all defects
SELECT * FROM Defects;

-- 2. Count total defects
SELECT COUNT(*) as TotalDefects FROM Defects;

-- 3. View recent imports
SELECT * FROM Defects WHERE ImportedDate >= DATEADD(DAY, -7, GETDATE());


-- ============================================
-- SUMMARY STATISTICS
-- ============================================

-- 4. Defects by Project
SELECT Project, COUNT(*) as DefectCount
FROM Defects
GROUP BY Project
ORDER BY DefectCount DESC;

-- 5. Defects by MES_Fail_Category
SELECT MES_Fail_Category, COUNT(*) as DefectCount
FROM Defects
WHERE MES_Fail_Category IS NOT NULL
GROUP BY MES_Fail_Category
ORDER BY DefectCount DESC;

-- 6. Defects by MES_DDS_Category
SELECT MES_DDS_Category, COUNT(*) as DefectCount
FROM Defects
WHERE MES_DDS_Category IS NOT NULL
GROUP BY MES_DDS_Category
ORDER BY DefectCount DESC;

-- 7. Defects by Stage
SELECT Stages, COUNT(*) as DefectCount
FROM Defects
WHERE Stages IS NOT NULL
GROUP BY Stages
ORDER BY DefectCount DESC;

-- 8. Defects by Location
SELECT MES_Location, COUNT(*) as DefectCount
FROM Defects
WHERE MES_Location IS NOT NULL
GROUP BY MES_Location
ORDER BY DefectCount DESC;


-- ============================================
-- DETAILED ANALYSIS
-- ============================================

-- 9. Defects by Project and Category
SELECT Project, MES_Fail_Category, COUNT(*) as DefectCount
FROM Defects
GROUP BY Project, MES_Fail_Category
ORDER BY Project, DefectCount DESC;

-- 10. Top 10 most common defects
SELECT TOP 10 Trace_Defect, COUNT(*) as Occurrences
FROM Defects
WHERE Trace_Defect IS NOT NULL
GROUP BY Trace_Defect
ORDER BY Occurrences DESC;

-- 11. Top 10 most common failures
SELECT TOP 10 MES_Failure, COUNT(*) as Occurrences
FROM Defects
WHERE MES_Failure IS NOT NULL
GROUP BY MES_Failure
ORDER BY Occurrences DESC;

-- 12. Cross-tab: Project vs Category
SELECT 
    Project,
    SUM(CASE WHEN MES_Fail_Category = 'DDS' THEN 1 ELSE 0 END) as DDS_Count,
    SUM(CASE WHEN MES_Fail_Category = 'Non_DDS' THEN 1 ELSE 0 END) as Non_DDS_Count,
    COUNT(*) as Total
FROM Defects
WHERE Project IS NOT NULL AND MES_Fail_Category IS NOT NULL
GROUP BY Project
ORDER BY Total DESC;


-- ============================================
-- SEARCH QUERIES
-- ============================================

-- 13. Find specific defect by name
SELECT * FROM Defects
WHERE Trace_Defect LIKE '%Bubble%'
ORDER BY Project;

-- 14. Find defects in specific location
SELECT * FROM Defects
WHERE MES_Location LIKE '%BGA%'
ORDER BY Project;

-- 15. Find all DDS category defects
SELECT * FROM Defects
WHERE MES_DDS_Category = 'DDS'
ORDER BY Project, Trace_Defect;

-- 16. Find all Non_DDS category defects
SELECT * FROM Defects
WHERE MES_DDS_Category = 'Non_DDS'
ORDER BY Project, Trace_Defect;


-- ============================================
-- DATA QUALITY CHECKS
-- ============================================

-- 17. Check for missing values
SELECT 
    SUM(CASE WHEN Project IS NULL THEN 1 ELSE 0 END) as Missing_Project,
    SUM(CASE WHEN Trace_Defect IS NULL THEN 1 ELSE 0 END) as Missing_Trace_Defect,
    SUM(CASE WHEN MES_Failure IS NULL THEN 1 ELSE 0 END) as Missing_MES_Failure,
    SUM(CASE WHEN MES_Location IS NULL THEN 1 ELSE 0 END) as Missing_MES_Location,
    SUM(CASE WHEN MES_Fail_Category IS NULL THEN 1 ELSE 0 END) as Missing_MES_Fail_Category,
    SUM(CASE WHEN MES_DDS_Category IS NULL THEN 1 ELSE 0 END) as Missing_MES_DDS_Category,
    SUM(CASE WHEN Stages IS NULL THEN 1 ELSE 0 END) as Missing_Stages
FROM Defects;

-- 18. Check for duplicate entries
SELECT Trace_Defect, Project, COUNT(*) as Count
FROM Defects
GROUP BY Trace_Defect, Project
HAVING COUNT(*) > 1
ORDER BY Count DESC;

-- 19. List unique values for each category
SELECT DISTINCT Project FROM Defects WHERE Project IS NOT NULL ORDER BY Project;
SELECT DISTINCT MES_Fail_Category FROM Defects WHERE MES_Fail_Category IS NOT NULL ORDER BY MES_Fail_Category;
SELECT DISTINCT MES_DDS_Category FROM Defects WHERE MES_DDS_Category IS NOT NULL ORDER BY MES_DDS_Category;
SELECT DISTINCT Stages FROM Defects WHERE Stages IS NOT NULL ORDER BY Stages;


-- ============================================
-- MAINTENANCE QUERIES
-- ============================================

-- 20. Delete duplicate records (keep first occurrence)
DELETE FROM Defects
WHERE DefectID NOT IN (
    SELECT MIN(DefectID)
    FROM Defects
    GROUP BY Trace_Defect, Project
);

-- 21. Update records (example - change DDS category)
-- UPDATE Defects
-- SET MES_DDS_Category = 'DDS'
-- WHERE MES_Fail_Category = 'Critical';

-- 22. Export defects to backup (create copy)
SELECT * INTO Defects_Backup FROM Defects;

-- 23. Get import statistics
SELECT 
    COUNT(*) as Total_Records,
    MIN(ImportedDate) as First_Import,
    MAX(ImportedDate) as Last_Import,
    COUNT(DISTINCT Project) as Unique_Projects
FROM Defects;

-- 24. Clear old data (if needed - USE WITH CAUTION)
-- DELETE FROM Defects WHERE ImportedDate < DATEADD(MONTH, -6, GETDATE());

-- 25. Drop table (if you need to start fresh - USE WITH EXTREME CAUTION)
-- DROP TABLE Defects;


-- ============================================
-- TIPS FOR USE
-- ============================================
-- 1. Replace 'Defects' with your actual table name if different
-- 2. Adjust date ranges and conditions as needed
-- 3. Always back up before running DELETE or UPDATE statements
-- 4. Use TOP N to limit large result sets
-- 5. Use LIKE '%text%' for partial matches
-- 6. Use IS NULL / IS NOT NULL to check for empty values
