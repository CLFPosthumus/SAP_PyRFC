from SAP_PyRFC import main

sap = main()

transport = ['DA12345678']

# Create an SQL Query to retrieve the creation date of the transports in transport variable (from the E070 table in SAP)

#Create query on fieldname TRKORR (transport)
Where = sap.whereclauses(fieldname='TRKORR',qrylist=listoftransports)

#Use the ware clause the retrieve the AS4DATE field from each transport in the list
creationdatedict = sap.qry(Fields=['AS4DATE'],SQLTable='E070',Where=Where)

#Parse the timestamp retrieved fromt the query
datetime = parse(creationdatedict['AS4DATE'][0])


#Get tranports after this date
#Get 1/2 year before transport creation date
newdate = datetime-timedelta(6 * 365 / 12)

#reformat the datetime to a SQL readable string
newdate = "{0}{1:02d}{2:02d}".format(newdate.year,newdate.month,newdate.day)

#Create a single whereclause to query all transports before newdate
Where = ["AS4DATE > '{0}'".format(newdate)]

#Query SAP to get all transports using the whereclause created earlier
transportdict = sap.qry(Fields=['TRKORR'],SQLTable='E070',Where=Where)

if not transportdict['TRKORR'] == []:
    #Create a where clause that searches
    #for OBJECT field and a value of RSPC. This will return all process chain objects in your transport
    Where = sap.whereclauses(fieldname='TRKORR',qrylist=transport,andfield='OBJECT',andvalue='RSPC')
    #QRY table E071 to get all objects in your transport, use the where clause as filter. Will return the OBJECT and OBJ_NAME field and their values.
    dependencyobj = sap.qry(Fields=['OBJECT','OBJ_NAME'],SQLTable='E071',Where=Where)



    #Does the same as the above statement, only this time for all transports within the given timeframe.
    Where = sap.whereclauses(fieldname='TRKORR',qrylist=transportdict['TRKORR'],andfield='OBJECT',andvalue='RSPC')
    matchobjects = sap.qry(Fields=['OBJ_NAME','TRKORR'], SQLTable='E071', Where=Where)

    #CHECK ALL TRANSPORTS FOR DEPENDENT OBJECTS
    if matchobjects['OBJ_NAME'] == []:
        print('NO RSPC OBJECTS FOUND IN NEWER TRANSPORTS')
    else:
        matches = (sap.compare_intersect(matchobjects['OBJ_NAME'],dependencyobj['OBJ_NAME']))
        if not matches == []:
            keydict = dict(zip(matchobjects['OBJ_NAME'], matchobjects['TRKORR']))
            dependendtransports = set([keydict[x] for x in keydict if x in matches])
            print ('Found {0} object contentions in transports'.format(len(dependendtransports)))
            for x in dependendtransports:
                print('Transport: {0}'.format(x))
            for x in matches:
                print('Matching object: {0}'.format(x))

        pass


print('Done')