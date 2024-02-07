import datetime, sys, os # Importing OS, Sys, date time libraries used for things like navigating folders, creating timestamps etc. 
import csv # Library used to read/write csv files
import glob # It is useful in any situation where your program needs to look for a list of files on the filesystem with names matching a pattern. 
import os.path # This module implements some useful functions on pathnames. To read or write files see open(), and for accessing the filesystem see the os module. The path parameters can be passed as either strings, or bytes.
from utils.path_generator import getBaseNamespaces, process # Importing two methods from path_generator file
from utils.logging import Error_Details, log_access, log_error, log_schema_error # Importing custom error logger Function, and Error Details Class
from settings import files, mapping_location, schemas_location # Import all variables that are hardcoded 

# Store name of current script in Error_Details class object as script name. We do this so that error log will always tell us which script error comes from. 
Error_Details.script = os.path.split(sys.argv[0])[1]

lines = [] # This is the final container which will have variables with details  i.e. the mapping -> its a list of lists -> ['2018v1.0', 'IRS990ScheduleD', 'Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt', 'USAmountType', 'Donated services and use of facilities', 'Part XI Line 2b', '0', None]

def main():

    '''
    Main Function: 
    1. Processes Schemas
    2. Creates variables from schemas
    3. Stores variables with details on a csv called mapping_date.csv in output folder 
       - i.e. CSV has following columns: "Version","Source","Xpath","Type","Description","Line","MinOccur","MaxOccur"
    '''
    print ("Initiating Schema Mapper")
    log_access('', 'Initiating Schema Mapper', Error_Details)

    # Step 1. Find all schema folders in schema/current folder  and store as a list of paths example -> '../schemas/all/2018v1.0'
    print ('Finding all schemas')
    try:
      schemas = glob.glob(schemas_location)
    except Exception as e:
      print("Error with grabbing schemas. Check location and make sure you have a folder(s) called schemas/all in repository", e)
      log_error(e, "Error with grabbing schemas from schemas/all", Error_Details)      

    # Step 2. For each path path of schemas. 
    print ('Processing schemas')
    for schema in schemas:
        print ("Processing %s" % schema)

        # Step 2b. Get namespaces from the common-efiletypes file by passing version -> which is a path  like this -> '../schemas/all/2018v1.0'
        # return a dictionary containing results as such 'IPAddressType': set([<path_generator.Node instance at 0x109cb91b8>, <path_generator.Node instance at 0x109cb9170>]),
        try:
         namespaces = getBaseNamespaces(schema)
        except Exception as e:
         print("Error grabbing name spaces for %s" %schema, e)
         log_schema_error(e, "Error grabbing name spaces for %s" %schema, Error_Details)        

        # Steb 2c. # for each of the files listed to process
        for fn in files:

            # Step 2c2. Create a path with version '../schemas/all/2018v1.0' and file "TEGE/TEGE990/IRS990/IRS990.xsd"
            # Path will look like this: ../schemas/all/2018v1.0/TEGE/Common/Dependencies/GeneralExplanationAttachment.xsd
            path = "%s/%s" % (schema, fn)

            # Step 2c3. Check to see if path exists (i.e. if it is viable)
            if os.path.exists(path):

                # Step 2c3b. Set xpref to value of the keyfile
                # Should look like this -> "Return/ReturnData"
                xpref = files[fn]

                # Step 2c3c. Call process function passing
                '''  
                1. dictionary of basenamespaces i.e. common efile types, 
                2. prefix type "Return/ReturnData" or Return
                3. path to file ../schemas/all/2018v1.0/TEGE/Common/Dependencies/GeneralExplanationAttachment.xsd
                '''
                local = process(namespaces, xpref, path)
                
                final_local = []
                for local_lines in local: 
                  line = []
                  for l in local_lines:
                     if l is not None:
                        line.append(l.decode("utf-8"))
                     else:
                        line.append("None")
                  final_local.append(line)
                ## Step 2c3d take the lines container and extended by appending local 
                lines.extend(final_local)
            else:
               #print ("Schema  %s  does not exist: so it wont be processed." % path)
               log_schema_error('', "Schema %s does not exist so it wont be processed." % path, Error_Details)

    # Step 3. Make CSV within folder called output/xpath_all 
    print ('Making mapping.csv in /output folder.')
    try: 
       with open(mapping_location, "w") as outfile:

           # Set out as the file
           out = csv.writer(outfile)

           # Create a header with following columns
           header = ["Version","Source","Xpath","Type","Description","Line","MinOccur","MaxOccur"]
           out.writerow(header)

           # Append rows from lines list to form csv
           try:
            out.writerows(lines)
           except Exception as e:
            print("Error with writing rows", e)
            log_error(e, "Error with writing rows to csv", Error_Details)
    
    except Exception as e: 
      print("Error with making mapping.csv", e)
      log_error(e, "Error with making mapping.csv", Error_Details)
    
    # Step 4. Finished
    print ("Schema Mapper is Finished Running. Check output/mapping_[date].csv for created file. ")
    log_access('', 'Schema Mapper is Finished Running. Check output/mapping_[date].csv for created file.', Error_Details)

if __name__ == "__main__":
   # Call the main function
   main()



