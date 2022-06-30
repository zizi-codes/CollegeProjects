use NYDOH; 
select * from NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results;

/*insert into NYDOH_dw.Restaurant
(CAMIS, DBA, BUILDING, STREET, PHONE, Latitude, Longitude)

select DISTINCT CAMIS, DBA, BUILDING, STREET, PHONE, Latitude, Longitude from NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results 
ORDER BY CAMIS DESC;
*/

/*
insert into NYDOH_dw.Location
(BORO, ZIPCODE)

SELECT DISTINCT BORO, ZIPCODE FROM NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results
order by BORO
*/

/*
insert into NYDOH_dw.Violation
(VIOLATION_CODE, VIOLATION_DESCRIPTION)

SELECT DISTINCT VIOLATION_CODE, VIOLATION_DESCRIPTION FROM NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results
*/

/*
insert into NYDOH_dw.Cuisine
(CUISINE_DESCRIPTION)

SELECT DISTINCT CUISINE_DESCRIPTION FROM NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results
*/

/*
ALTER TABLE NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results
ADD INSPECTION_DATE_Clean DATETIME;

Update NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results set INSPECTION_DATE_Clean = STR_TO_DATE(INSPECTION_DATE,'%m/%d/%Y');
*/

/*
insert into NYDOH_dw.Date
(idDate, INSPECTION_DATE, YEAR, QUARTER, MONTH, DAY)
select DISTINCT date_format(INSPECTION_DATE_Clean,'%Y%m%d'), INSPECTION_DATE_Clean,  YEAR(INSPECTION_DATE_Clean), QUARTER(INSPECTION_DATE_Clean), 
				MONTH(INSPECTION_DATE_Clean),DAY(INSPECTION_DATE_Clean)
from NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results;
*/

/* 
FACT TABLE - Incomplete- don't run yet 
*/
insert into NYDOH_dw.Inspection_Results
(CAMIS, INSPECTION_DATE, ACTION, CRITICAL_FLAG, SCORE, GRADE, GRADE_DATE, RECORD_DATE,
INSPECTION_TYPE, Community_Board, Council_District, Census_Tract, BIN, BBL, NTA, 
Location_idLocation, Restaurant_CAMIS, Cuisine_idCuisine, Date_idDate, Violation_idViolation)
 
select 
db.CAMIS, db.INSPECTION_DATE, db.ACTION, db.CRITICAL_FLAG, db.SCORE, db.GRADE, db.GRADE_DATE, db.RECORD_DATE,
db.INSPECTION_TYPE, db.Community_Board, db.Council_District, db.Census_Tract, db.BIN, db.BBL, db.NTA, 
dwl.idLocation, dwr.CAMIS, Cuisine_idCuisine, Date_idDate, Violation_idViolation

from NYDOH.DOHMH_New_York_City_Restaurant_Inspection_Results db
INNER JOIN NYDOH_dw.Cuisine dwc ON db.CUISINE_DESCRIPTION = dwc
INNER JOIN NYDOH_dw.Violation dwv ON db.VIOLATION_CODE = dwv
INNER JOIN NYDOH_dw.Location dwl ON db.__ = dwl
INNER JOIN NYDOH_dw.Restaurant dwr ON db.CAMIS = dwr.
INNER JOIN NYDOH_dw.Date dwd ON db.INSPECTION_DATE_Clean = dwd.Date; 

/* Fact table from PPPLoan Dataset

insert into ppploan_dw.cis4440
 (LoanNumber, DateApproved, ProcessingMethod, LoanStatusDate, LoanStatus, Term, SBAGuarantyPercentage, InitialApprovalAmount, 
 CurrentApprovalAmount, UndisbursedAmount, ServicingLenderName, ProjectCountyName, NAICSCode, Race, Ethnicity, UTILITIES_PROCEED, 
 PAYROLL_PROCEED, MORTGAGE_INTEREST_PROCEED, RENT_PROCEED, REFINANCE_EIDL_PROCEED, HEALTH_CARE_PROCEED, DEBT_INTEREST_PROCEED, 
 OriginatingLender, ForgivenessAmount, ForgivenessDate, borrower_idBorrower, originallender_idOriginalLender, office_idOffice, 
 servicelender_idServiceLender, project_idProject, date_idDate)
select 
cis.LoanNumber, cis.dateApprovedClean, cis.ProcessingMethod, cis.LoanStatusDate, cis.LoanStatus, cis.Term, cis.SBAGuarantyPercentage, 
cis.InitialApprovalAmount, cis.CurrentApprovalAmount, cis.UndisbursedAmount, cis.ServicingLenderName, cis.ProjectCountyName, 
cis.NAICSCode, cis.Race, cis.Ethnicity, cis.UTILITIES_PROCEED, cis.PAYROLL_PROCEED, cis.MORTGAGE_INTEREST_PROCEED, cis.RENT_PROCEED, 
cis.REFINANCE_EIDL_PROCEED, cis.HEALTH_CARE_PROCEED, cis.DEBT_INTEREST_PROCEED, cis.OriginatingLender, cis.ForgivenessAmount, 
cis.ForgivenessDate, dwb.idBorrower, dwol.idOriginalLender, dwo.idOffice, dwsl.idServiceLender, 
dwp.idProject, dwd.idDate
from ppploan.cis4440  cis 
INNER JOIN ppploan_dw.project dwp ON cis.ProjectCountyName = dwp.ProjectName
INNER JOIN ppploan_dw.office dwo ON cis.SBAOfficeCode = dwo.SbaofficeCode
INNER JOIN ppploan_dw.servicelender dwsl ON cis.ServicingLenderName = dwsl.ServicingLenderName
INNER JOIN ppploan_dw.originallender dwol ON cis.OriginatingLender = dwol.OriginatingLender
INNER JOIN ppploan_dw.borrower dwb ON cis.BorrowerName = dwb.BorrowerName
INNER JOIN ppploan_dw.date dwd ON cis.dateApprovedClean = dwd.Date; 
*/