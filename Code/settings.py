from datetime import datetime

### This file contains all settings used by the Mapper Library

time = str(datetime.now()).split(' ')[0]

# Mapping File Location
mapping_location = "../Output/mapping_%s.csv" % time

# Schema Folder: This is where all schemas should be located
schemas_location = "../Input/Schemas/all/*"

# List of files in TEGE (Tax Exempt Groups Entities) Uncomment all of the ones you wish to process. We recommend uncommenting all of them.  
files = {#Schema Files 																		              # XML Path
         "TEGE/TEGE990/IRS990/IRS990.xsd" :                                              "Return/ReturnData",
         "TEGE/TEGE990/IRS990/AffiliateListing.xsd" :                                    "Return/ReturnData",
         "TEGE/TEGE990/IRS990/CashGrantsPaidSchedule.xsd" :                              "Return/ReturnData",
         "TEGE/TEGE990/IRS990/CompensationSchedule.xsd" :                                "Return/ReturnData",
         "TEGE/TEGE990/IRS990/DAFCashGrantsPaidSchedule.xsd" :                           "Return/ReturnData",
         "TEGE/TEGE990/IRS990/DAFNoncashGrantsPaidSchedule.xsd" :                        "Return/ReturnData",
         "TEGE/TEGE990/IRS990/DepreciationAndDepletionSchedule.xsd":                     "Return/ReturnData",
         "TEGE/TEGE990/IRS990/DisqualifiedPersonSchedule.xsd":                           "Return/ReturnData",
         "TEGE/TEGE990/IRS990/IndividualAssistanceSchedule.xsd" :                        "Return/ReturnData",
         "TEGE/TEGE990/IRS990/InvestmentsLandSchedule.xsd" :                             "Return/ReturnData",
         "TEGE/TEGE990/IRS990/InvestmentsOtherSchedule.xsd" :                            "Return/ReturnData",
         "TEGE/TEGE990/IRS990/InvestmentsSecuritiesSchedule.xsd" :                       "Return/ReturnData",
         "TEGE/TEGE990/IRS990/LandEtcSchedule.xsd" :                                     "Return/ReturnData",
         "TEGE/TEGE990/IRS990/MemberBenefitsSchedule.xsd" :                              "Return/ReturnData",
         "TEGE/TEGE990/IRS990/NoncashGrantsPaidSchedule.xsd" :                           "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherAssetsSchedule2.xsd" :                                "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherExpensesIncludedSchedule.xsd" :                       "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherExpensesNotIncludedSchedule.xsd" :                    "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherInvestmentIncomeSchedule.xsd" :                       "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherLiabilitiesSchedule2.xsd" :                           "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherNotesLoansReceivableShortSchedule.xsd" :              "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherRevenuesIncludedSchedule.xsd" :                       "Return/ReturnData",
         "TEGE/TEGE990/IRS990/OtherRevenuesNotIncludedSchedule.xsd" :                    "Return/ReturnData",
         "TEGE/TEGE990/IRS990/PaymentToAffiliatesSchedule.xsd" :                         "Return/ReturnData",
         "TEGE/TEGE990/IRS990/RelationshipSchedule.xsd" :                                "Return/ReturnData",
         "TEGE/TEGE990/IRS990/TaxExemptBondLiabilitiesSchedule.xsd" :                    "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/IRS990EZ.xsd" :                                        "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/ExplanationOfNonUBI.xsd" :                             "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/GrantsAndSimilarAmountsPaidSchedule.xsd" :             "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/LoansToFromOfficersSchedule.xsd" :                     "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/OtherAssetsSchedule3.xsd" :                            "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/OtherExpensesSchedule2.xsd" :                          "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/OtherLiabilitiesSchedule3.xsd" :                       "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/OtherRevenuesSchedule2.xsd" :                          "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/ProxyTaxExplanation.xsd" :                             "Return/ReturnData",
         "TEGE/TEGE990EZ/IRS990EZ/TransfersPersonalBenefitsContractsDeclaration.xsd" :   "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/IRS990PF.xsd" :                                        "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/AccountingFeesSchedule.xsd" :                          "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/ActivitiesNotPreviouslyReportedExplanation.xsd" :      "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/AllOtherProgramRelatedInvestmentsSchedule.xsd" :       "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/AmortizationSchedule.xsd" :                            "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/AppliedToPriorYearElection.xsd" :                      "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/BorrowedFundsElection.xsd" :                           "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/CashDeemedCharitableExplanationStatement.xsd" :        "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/CashDistributionExplanationStatement.xsd" :            "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/DepreciationSchedule.xsd" :                            "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/DissolutionStatement.xsd" :                            "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/DistributionFromCorpusElection.xsd" :                  "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/DonorAdvisedFundStatement.xsd" :                       "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/EmployeeCompensationExplanation.xsd" :                 "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/ExpenditureResponsibilityStatement.xsd" :              "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/ExplanationOfLegisPoliticalActivities.xsd" :           "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/ExplanationOfNonFilingWithAGStatement.xsd" :           "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/GainLossFromSaleOtherAssetsSchedule.xsd" :             "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/GeneralExplanationAttachment.xsd" :                    "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/InvestmentsCorpBondsSchedule.xsd" :                    "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/InvestmentsCorpStockSchedule.xsd" :                    "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/InvestmentsGovtObligationsSchedule.xsd" :              "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/InvestmentsLandSchedule2.xsd" :                        "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/InvestmentsOtherSchedule2.xsd" :                       "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/LandEtcSchedule2.xsd" :                                "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/LegalFeesSchedule.xsd" :                               "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/LiquidationExplanationStatement.xsd" :                 "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/LoansFromOfficers.xsd" :                               "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/MortgagesandNotesPayable.xsd" :                        "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherAssetsSchedule.xsd" :                             "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherDecreasesSchedule.xsd" :                          "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherExpensesSchedule.xsd" :                           "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherIncomeSchedule2.xsd" :                            "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherIncreasesSchedule.xsd" :                          "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherLiabilitiesSchedule.xsd" :                        "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherNotesLoansReceivableShortSchedule2.xsd" :         "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherProfessionalFeesSchedule.xsd" :                   "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/OtherReceivablesFromOfficers.xsd" :                    "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/ReasonableCauseExplanation.xsd" :                      "Return/ReturnData",         
         "TEGE/TEGE990PF/IRS990PF/ReductionExplanationStatement.xsd" :                   "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/RelationshipSchedule.xsd" :                            "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/SalesOfInventorySchedule.xsd" :                        "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/Section4942a2ExplanationStatement.xsd" :               "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/SubstantialContributorsSchedule.xsd" :                 "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/TaxesSchedule.xsd" :                                   "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/TaxUnderSection511Statement.xsd" :                     "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/TransfersFromControlledEntitiesSchedule.xsd" :         "Return/ReturnData",
         "TEGE/TEGE990PF/IRS990PF/TransfersToControlledEntitiesSchedule.xsd" :           "Return/ReturnData",
         "TEGE/Common/ReturnHeader990x.xsd" :                                            "Return"
         "TEGE/Common/Dependencies/ActivitiesNotPreviouslyReportedExplanation.xsd" :     "Return/ReturnData",
         "TEGE/Common/Dependencies/AffiliateListing.xsd" :                               "Return/ReturnData",
         "TEGE/Common/Dependencies/CompensationExplanation.xsd" :                        "Return/ReturnData",
         "TEGE/Common/Dependencies/ContractorCompensationExplanation.xsd" :              "Return/ReturnData",
         "TEGE/Common/Dependencies/ControlledEntitySchedule.xsd":                        "Return/ReturnData",
         "TEGE/Common/Dependencies/DissolutionStatement.xsd" :                           "Return/ReturnData",
         "TEGE/Common/Dependencies/EmployeeCompensationExplanation.xsd" :                "Return/ReturnData",
         "TEGE/Common/Dependencies/ExcessBenefitTransactionsStatement.xsd" :             "Return/ReturnData",
         "TEGE/Common/Dependencies/GainLossFromSaleNonpublicSecuritiesSchedule.xsd" :    "Return/ReturnData",
         "TEGE/Common/Dependencies/GainLossFromSaleOtherAssetsSchedule.xsd" :            "Return/ReturnData",
         "TEGE/Common/Dependencies/GainLossFromSalePublicSecuritiesSchedule.xsd" :       "Return/ReturnData",
         "TEGE/Common/Dependencies/GeneralExplanationAttachment.xsd" :                   "Return/ReturnData",
         "TEGE/Common/Dependencies/LiquidationExplanationStatement.xsd" :                "Return/ReturnData",
         "TEGE/Common/Dependencies/LoansFromOfficersSchedule.xsd" :                      "Return/ReturnData",
         "TEGE/Common/Dependencies/MortgagesAndNotesPayableSchedule.xsd" :               "Return/ReturnData",
         "TEGE/Common/Dependencies/OtherChangesInNetAssetsSchedule.xsd" :                "Return/ReturnData",
         "TEGE/Common/Dependencies/OtherNotesLoansReceivableLongSchedule.xsd" :          "Return/ReturnData",
         "TEGE/Common/Dependencies/OtherReceivablesFromOfficersSchedule.xsd" :           "Return/ReturnData",
         "TEGE/Common/Dependencies/ReasonableCauseExplanation.xsd" :                     "Return/ReturnData",
         "TEGE/Common/Dependencies/RequestForCopyAttachment.xsd" :                       "Return/ReturnData",
         "TEGE/Common/Dependencies/SalesOfInventorySchedule.xsd" :                       "Return/ReturnData",
         "TEGE/Common/Dependencies/SpecialEventsSchedule.xsd" :                          "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/IRS990ScheduleA.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/AffiliatedGroupAttachment.xsd" :                   "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/AffiliatedGroupSchedule.xsd" :                     "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/AveragingAttachment.xsd" :                         "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/ComplianceWithRevProc75_50Explanation.xsd" :       "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/ConservationEasements.xsd" :                       "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/ExplnOfReceiptOrRevocationOfGovtFinancialAid.xsd": "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/NonelectingPublicCharitiesStatement.xsd" :         "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/OtherIncomeSchedule.xsd" :                         "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/ScholarshipAwardStatement.xsd" :                   "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/SelfDealingStatement.xsd" :                        "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleA/SupplementalSupportSchedule.xsd" :                 "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleB/IRS990ScheduleB.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleC/IRS990ScheduleC.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleC/AffiliatedGroupAttachment.xsd" :                   "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleC/AffiliatedGroupSchedule.xsd" :                     "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleC/AveragingAttachment.xsd" :                         "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleD/IRS990ScheduleD.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleE/IRS990ScheduleE.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleF/IRS990ScheduleF.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleG/IRS990ScheduleG.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleH/IRS990ScheduleH.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleI/IRS990ScheduleI.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleJ/IRS990ScheduleJ.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleK/IRS990ScheduleK.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleL/IRS990ScheduleL.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleM/IRS990ScheduleM.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleN/IRS990ScheduleN.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleO/IRS990ScheduleO.xsd" :                             "Return/ReturnData",
         "TEGE/Common/IRS990ScheduleR/IRS990ScheduleR.xsd" :                             "Return/ReturnData",
         }
