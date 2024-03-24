-- ================================================
--A procedure to calculate prevalence rate per year, disease and age group
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Nika Paradina>
-- Create date: <2022-12-26>
-- Description:	<A procedure to calculate prevalnce raste per year, disease and age group>
-- =============================================

--- if procedure already exists, delete it
IF OBJECT_ID ( 'dbo.sp_prevalence_rates', 'P' ) IS NOT NULL
    DROP PROCEDURE dbo.sp_prevalence_rates;
GO


CREATE PROCEDURE dbo.sp_prevalence_rates

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	
	--- if table already exists, delete it
	IF OBJECT_ID ( 'dbo.prevalence_year_age_group', 'U' ) IS NOT NULL
    DROP TABLE dbo.prevalence_year_age_group;

	-- creates a table for calculated prevalence rates
	CREATE TABLE [dbo].[prevalence_year_age_group](
	[year] [int] NULL,
	[name_of_disease] [nvarchar](max) NULL,
	[code_MKB] [nvarchar](max) NULL,
	[age_group] [nvarchar](255) NULL,
	[prevalence_rate] [numeric](18, 2) NULL
	) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
	-- prevalence is calculated from morbidity and population data
	INSERT INTO [dbo].[prevalence_year_age_group]
				([year]
				,[name_of_disease]
				,[code_MKB]
				,[age_group]
				,[prevalence_rate])
			SELECT 
				m.[year],
				m.[name_of_disease],
				m.[code_MKB],
				m.[age_group],
				[prevalence_rate]=CAST(ROUND(m.[sum]/pop.[sum]*100,2,0) AS numeric (18, 2))-- as a two decimal percentage
			FROM [dbo].[morbidity_per_age_group_unpivot] m
			LEFT JOIN [dbo].[population_year_age_group] pop ON pop.year=m.year AND pop.age_group=m.age_group
END
GO
