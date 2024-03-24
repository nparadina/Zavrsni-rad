/****** Script for SelectTopNRows command from SSMS  ******/
BEGIN TRAN

SELECT * FROM [dbo].[second_age_group_sigmas] ORDER BY run DESC

DELETE FROM [dbo].[second_age_group_sigmas] WHERE run>=1000000

SELECT * FROM [dbo].[second_age_group_sigmas] ORDER BY run DESC

ROLLBACK
--COMMIT