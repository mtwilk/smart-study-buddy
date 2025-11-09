-- Clear all data from Supabase for fresh testing
-- Run this in Supabase SQL Editor

-- Delete in correct order to respect foreign key constraints

-- 1. Delete exercises (references study_sessions and assignments)
DELETE FROM exercises;

-- 2. Delete study sessions (references assignments)
DELETE FROM study_sessions;

-- 3. Delete user progress (references assignments)
DELETE FROM user_progress;

-- 4. Delete assignments (references profiles/users)
DELETE FROM assignments;

-- Optional: Reset sequences if you want IDs to start from 1 again
-- (Only if using SERIAL columns - Supabase usually uses UUID so this may not be needed)

-- Verify deletion
SELECT
    'exercises' as table_name, COUNT(*) as remaining_rows FROM exercises
UNION ALL
SELECT 'study_sessions', COUNT(*) FROM study_sessions
UNION ALL
SELECT 'user_progress', COUNT(*) FROM user_progress
UNION ALL
SELECT 'assignments', COUNT(*) FROM assignments;

-- You should see all counts as 0
