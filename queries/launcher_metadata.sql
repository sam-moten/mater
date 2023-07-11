WITH
  metadata AS (
  SELECT
    DISTINCT measures.id,
    measures.status,
    measures.muscles_right,
    measures.muscles_left,
    measures.code,
    CONCAT(SUBSTR(measures.code, 2,4),'-', SUBSTR(measures.code, 6,2), '-', SUBSTR(measures.code, 8,2)) AS date,
    CONCAT(SUBSTR(measures.code, 11,2), 'h', SUBSTR(measures.code, 13,2) ) AS time,
    subjects.name AS subject,
    projects.name AS PROJECT
  FROM
    {{project_id}}.METADATA.measures AS measures
  LEFT JOIN
    {{project_id}}.METADATA.subjects AS subjects
  ON
    subjects.id=measures.subject_id
  LEFT JOIN
    {{project_id}}.METADATA.projects AS projects
  ON
    projects.id=measures.project_id
  LEFT JOIN
    {{project_id}}.METADATA.companies AS companies
  ON
    companies.id=measures.company_id)
SELECT
  muscles_right, 
  muscles_left,
  CONCAT(subject,' / ', date,' ',time, ' / ',PROJECT) AS id,
  id as session
FROM
  metadata
WHERE
  1=1
  #and project="MATER" 
  #and status='1' 
ORDER BY
  date DESC,
  time DESC
    