/****** Script for SelectTopNRows command from SSMS  ******/
BEGIN TRAN

SELECT 
	*
FROM
	[Critical Illness insurance].[dbo].[morbidity_per_age_group];

WITH cte (year, name_of_disease, code_MKB, age_group, Sum) AS (
	SELECT year, name_of_disease, code_MKB, age_group, Sum FROM (
		SELECT 
			*
		FROM
			[Critical Illness insurance].[dbo].[morbidity_per_age_group]
	) tmp
	UNPIVOT
	(
		Sum for age_group IN 
		([0_6],[7_19],[20_64],[65+])
	) AS unpv
)

INSERT INTO [dbo].[morbidity_per_age_group_unpivot]
	SELECT * FROM cte

SELECT * FROM [dbo].[morbidity_per_age_group_unpivot]

ROLLBACK