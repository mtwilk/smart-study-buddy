-- Add material_content column to assignments table to store uploaded study materials
ALTER TABLE assignments ADD COLUMN IF NOT EXISTS material_content TEXT;

-- Add comment to explain the column
COMMENT ON COLUMN assignments.material_content IS 'Stores the actual study material content uploaded by the user for AI question generation';
