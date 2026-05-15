INSERT INTO experiment (
    subject_id,
    experiment_type_id,
    experiment_date,
    score
)
SELECT
    %(subject_id)s,
    et.experiment_type_id,
    %(experiment_date)s,
    %(score)s
FROM experiment_type et
WHERE LOWER(et.type_name) = LOWER(%(experiment_type)s)
RETURNING experiment_id;