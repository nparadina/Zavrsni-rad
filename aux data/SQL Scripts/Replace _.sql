/****** Script for SelectTopNRows command from SSMS  ******/
BEGIN TRAN

SELECT *  FROM [dbo].[morbidity_per_age_group_unpivot]

UPDATE [dbo].[morbidity_per_age_group_unpivot]
   SET [age_group] = REPLACE([age_group], '_','-')

SELECT *  FROM [dbo].[morbidity_per_age_group_unpivot]

COMMIT