
SELECT
    subject_id AS subject_id,
    subject_name AS subject_name,
    species_id AS species_id,
    date_of_birth AS date_of_birth
FROM subject
WHERE subject_name LIKE '%o%';