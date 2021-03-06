from modules.bullhorn.data import BullhornData


bh = BullhornData()

"""
# https://cls41.bullhornstaffing.com/BullhornSTAFFING/OpenWindow.cfm?Entity=JobOrder&id=14012
# single entity example
entity = 'JobOrder'
id = 14012
fields = ['id','title','dateLastModified']
response = bh.getEntityById(entity,id,fields)
print(response)
"""

"""
# search example
entity = 'JobOrder'
query = "dateLastModified:[0 TO *]"
fields = ['id','description','title','dateLastModified']
response = bh.searchEntity(entity, query, fields)
print(response)
"""

"""
# dump example
entity = 'JobOrder'
fields = ["id","description","title","dateLastModified"]
# invalid fields documented but API returns error saying invalid field: billingProfile, clientCorporationLine, jobCode, jobOrderIntegrations
fields = ["id","address","appointments","approvedPlacements","assignedUsers","benefits","billRateCategoryID","bonusPackage","branch","branchCode","businessSectors","categories","certificationGroups","certificationList","certifications","clientBillRate","clientContact","clientCorporation","correlatedCustomDate1","correlatedCustomDate2","correlatedCustomDate3","correlatedCustomFloat1","correlatedCustomFloat2","correlatedCustomFloat3","correlatedCustomInt1","correlatedCustomInt2","correlatedCustomInt3","correlatedCustomText1","correlatedCustomText2","correlatedCustomText3","correlatedCustomText4","correlatedCustomText5","correlatedCustomText6","correlatedCustomText7","correlatedCustomText8","correlatedCustomText9","correlatedCustomText10","correlatedCustomTextBlock1","correlatedCustomTextBlock2","correlatedCustomTextBlock3","costCenter","customDate1","customDate2","customDate3","customFloat1","customFloat2","customFloat3","customInt1","customInt2","customInt3","customText1","customText2","customText3","customText4","customText5","customText6","customText7","customText8","customText9","customText10","customText11","customText12","customText13","customText14","customText15","customText16","customText17","customText18","customText19","customText20","customTextBlock1","customTextBlock2","customTextBlock3","customTextBlock4","customTextBlock5","dateAdded","dateClosed","dateEnd","dateLastExported","dateLastModified","dateLastPublished","degreeList","description","durationWeeks","educationDegree","employmentType","externalCategoryID","externalID","feeArrangement","fileAttachments","hoursOfOperation","hoursPerWeek","interviews","isClientEditable","isDeleted","isInterviewRequired","isJobcastPublished","isOpen","isPublic","jobBoardList","location","markUpPercentage","notes","numOpenings","onSite","opportunity","optionsPackage","owner","payRate","placements","publicDescription","publishedCategory","publishedZip","reasonClosed","reportTo","reportToClientContact","responseUser","salary","salaryUnit","sendouts","shift","shifts","skillList","skills","source","specialties","startDate","status","submissions","tasks","taxRate","taxStatus","tearsheets","timeUnits","title","travelRequirements","type","usersAssigned","webResponses","willRelocate","willRelocateInt","willSponsor","workersCompRate","yearsRequired"]
response = bh.dumpEntity(entity, fields)
print(response)
"""
