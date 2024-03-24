/****** Script for SelectTopNRows command from SSMS  ******/
BEGIN TRAN

SELECT distinct [name_of_disease], code_MKB
	FROM [Critical Illness insurance].[dbo].[morbidity_per_age_group_unpivot]

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Akutni infarkt miokarda – Acute myocardial infarction'
WHERE [name_of_disease]='Akutni infarkt miokarda'

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Cerebrovaskularni inzult – Stroke'
WHERE ( [name_of_disease]='Cerebrovaskularni inzult - Stroke' OR [name_of_disease]='Cerebrovaskularni inzult')

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Ostale zloćudne novotvorine – Other malignant neoplasms'
WHERE [name_of_disease]='Ostale zloćudne novotvorine'

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Zloćudna novotvorina dojke – Malignant neoplasm of breast'
WHERE [name_of_disease]='Zloćudna novotvorina dojke'

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Zloćudna novotvorina dušnika (traheje), dušnice (bronha) i pluća – Malignant neoplasm of trachea, bronchus and lung'
WHERE ([name_of_disease]='Zloćudna novotvorina dušnika (traheje), dušnice (bronha) i pluća' OR [name_of_disease]='Zloćudna novotvorina dušnika (traheje), dušnice (bronha) i pluća – Malignant neoplasm of trachea, broncuh and lung')

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Zloćudna novotvorina vrata maternice – Malignant neoplasm of cervix uteri'
WHERE [name_of_disease]='Zloćudna novotvorina vrata maternice'

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Zloćudna novotvorina završnog debelog crijeva (rektuma) – Malignant neoplasm of rectum'
WHERE [name_of_disease]='Zloćudna novotvorina završnog debelog crijeva (rektuma)'

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Zloćudne novotvorine limfnoga, hematopoetičnog i srodnog tkiva – Malignant neoplasm of lymphoid, hematopoietic and related tissue'
WHERE [name_of_disease]='Zloćudne novotvorine limfnoga, hematopoetičnog i srodnog tkiva'

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Zloćudna novotvorina želuca – Malignant neoplasm of stomach'
WHERE [name_of_disease]='Zloćudna novotvorina želuca'

UPDATE [dbo].[morbidity_per_age_group_unpivot]
SET [name_of_disease]='Zloćudni melanom kože – Malignant melanoma of skin'
WHERE [name_of_disease]='Zloćudni melanom kože'

SELECT distinct [name_of_disease], code_MKB
	FROM [Critical Illness insurance].[dbo].[morbidity_per_age_group_unpivot]

COMMIT