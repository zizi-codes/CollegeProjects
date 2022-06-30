use ppploan; 
select * from cis4440;
/*
insert into charliesangels_ppploan_dw.borrower
(BorrowerName, BorrowerCity, BorrowerState, BorrowerZip, FranchiseName,
BusinessAgeDescription, Gender, Veteran, NonProfit, RuralUrbanIndicator, HubzoneIncator, 
LMIIndicator, JobsReported, Race, Ethnicity, BusinessType)
select DISTINCT BorrowerName, BorrowerCity, BorrowerState, BorrowerZip, FranchiseName,
BusinessAgeDescription, Gender, Veteran, NonProfit, RuralUrbanIndicator, HubzoneIndicator,     
LMIIndicator, JobsReported, Race, Ethnicity, BusinessType from ppploan.cis4440 ORDER BY BorrowerName DESC;

insert into charliesangels_ppploan_dw.originallender
(OriginalLenderLocationID,OriginatingLender,OriginatingLenderCity,OriginatingLenderState)
Select DISTINCT OriginatingLenderLocationID,OriginatingLender, OriginatingLenderCity,OriginatingLenderState
from ppploan.cis4440;

insert into ppploan_dw.servicelender
(ServiceLenderLocation, ServicingLenderName, ServicingLendendAddress, ServicingLenderCity, ServiceLenderState, ServiceLenderZip)
Select DISTINCT  ServicingLenderLocationID, ServicingLenderName, ServicingLenderAddress, ServicingLenderCity, ServicingLenderState, ServicingLenderZip
from ppploan.cis4440;
*/
/*
insert into charliesangels_ppploan_dw.project
(ProjectCity, ProjectName, ProjectState, ProjectZip, CD)
Select DISTINCT  ProjectCity, ProjectCountyName, ProjectState, ProjectZip, CD
from ppploan.cis4440;

insert into charliesangels_ppploan_dw.office
(SbaofficeCode)
Select DISTINCT SBAOfficeCode 
from ppploan.cis4440;
*/

/*
ALTER TABLE ppploan.cis4440
ADD dateApprovedClean DATETIME;

Update ppploan.cis4440 set dateApprovedClean = STR_TO_DATE(DateApproved,'%m/%d/%Y');
*/

/*
insert into charliesangels_ppploan_dw.date
(idDate,Date, Year, Quarter, Month, Day)
select DISTINCT date_format(dateApprovedClean,'%Y%m%d'), dateApprovedClean,  YEAR(dateApprovedClean), QUARTER(dateApprovedClean), MONTH(dateApprovedClean),DAY(dateApprovedClean)
from ppploan.cis4440;

*/

insert into charliesangels_ppploan_dw.cis4440
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
