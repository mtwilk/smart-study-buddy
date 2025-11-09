-- Fix existing assignments with split topics by merging them into single topics
-- This migration finds assignments where topics are split (multiple short topics)
-- and merges them into a single topic

DO $$
DECLARE
    assignment_record RECORD;
    session_record RECORD;
    merged_topic TEXT;
    topic_array TEXT[];
    assignments_fixed INT := 0;
    sessions_fixed INT := 0;
BEGIN
    -- Fix assignments
    FOR assignment_record IN
        SELECT id, title, topics
        FROM assignments
        WHERE array_length(topics, 1) > 1
    LOOP
        -- Check if topics look split (average length < 15 chars suggests they were split)
        -- Calculate average topic length
        IF (
            SELECT AVG(LENGTH(topic))
            FROM unnest(assignment_record.topics) AS topic
        ) < 15 THEN
            -- Merge topics back together
            merged_topic := array_to_string(assignment_record.topics, ' ');
            topic_array := ARRAY[merged_topic];

            -- Update the assignment
            UPDATE assignments
            SET topics = topic_array
            WHERE id = assignment_record.id;

            RAISE NOTICE 'Fixed assignment %: % -> %',
                assignment_record.title,
                assignment_record.topics,
                topic_array;

            assignments_fixed := assignments_fixed + 1;
        END IF;
    END LOOP;

    -- Fix study sessions with the same logic
    FOR session_record IN
        SELECT id, topics
        FROM study_sessions
        WHERE array_length(topics, 1) > 1
    LOOP
        IF (
            SELECT AVG(LENGTH(topic))
            FROM unnest(session_record.topics) AS topic
        ) < 15 THEN
            -- Merge topics back together
            merged_topic := array_to_string(session_record.topics, ' ');
            topic_array := ARRAY[merged_topic];

            -- Update the session
            UPDATE study_sessions
            SET topics = topic_array
            WHERE id = session_record.id;

            sessions_fixed := sessions_fixed + 1;
        END IF;
    END LOOP;

    RAISE NOTICE 'Migration complete: Fixed % assignments and % study sessions',
        assignments_fixed, sessions_fixed;
END $$;
