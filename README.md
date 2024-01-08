
# IRS Form 990 Efile Schema to Data Dictionary Mapper

## Background

Every year all charities in the United States must file their annual tax returns (i.e Form 990) electronically with the IRS. This process is known as "efiling" a tax return which is similar to individuals using TurboTax (and other tools) to file their tax returns. 

Form 990s are considered public documents (i.e. open for public inspection) and the IRS releases these efiled forms as XML files on the IRS website https://www.irs.gov/charities-non-profits/form-990-series-downloads

Unfortunately, the different types of XML documents (across years and form types) as well as the XML format itself makes it difficult for various stakeholders - charities, researchers, businesses, and regulators - to extract the underlying data. 

These issus are complicated by shifting xpaths.  XML field locations can change (across years) as schemas are changed by the IRS.  For example, trying to grab a specifc field of the form 990 in 2010 will result in having to parse/navigate a Xpath that is different than the Xpath for the exact same field in 2018 as the xml schemas have changed. (See sample schemas --->  https://www.irs.gov/e-file-providers/current-valid-xml-schemas-and-business-rules-for-exempt-organizations-and-other-tax-exempt-entities-modernized-e-file).


### Our Goal: A software library that will: 

- Create a data dictionary (csv file) of xpaths (paths to specific form fields) from the underlying IRS XML Schemas for all fields of the Forms 990, 990ez, 990pf as well as schedules. This data dictionary can then be used to parse the XML files and grab the underlying data.

- Provide basic descriptive information (i.e. columns in the csv) for each field including: 
  - Schema Version 
  - Source
  - Field XPath
  - Field Type
  - Field Description
  - Line/Part of Form
  - Minimum Number of Occurences
  - Maximum Number of Occurences

### How The Schema Mapper Works

The mapper works by:
  - Scanning a directory containing all xml schemas folders
  - Processing each schema file (i.e IRS990.xsd) - by grabbing each element of the schema and pulling various attributes (name, description, line number). 
  - Storing all processed elements and details in a csv called: mapping_[date script was run].csv

**Example**:  The following is an element from a typical schema (in this case IRS990.XSD). The mapper would automatically pull the Element Name (WebsiteAddressTxt), Description (Web Site), LineNumber (J), and Min & Max Occur (which in this example don't exist)
  ``` 
    <xsd:element name="WebsiteAddressTxt" type="LineExplanationType" minOccurs="0">

      <xsd:annotation>

        <xsd:documentation>

          <Description>Web site</Description>

          <LineNumber>J</LineNumber>

        </xsd:documentation>

      </xsd:annotation>

    </xsd:element>
  ```

**Library Components**:
- Schema Files/Folders - Contain year by year list of all schemas
- Mapper - controlled by Main.py which executes path_generator.py 
- Logger - Tracks any errors

 **Critical Files**

The following are necessary for the mapper to work. 

 - Code/settings.py - contains all settings for the mapper. Particularly critical is the files dictionary containing all the schemas which are parsed year by year (and version by version) along with main xml path
 - Schemas/all/ - Contains a folder for each year and version of the schemas. 
    - Its very important that you have the schema folders organized in the same manner as the settings.py otherwise the code will fail. 
  - We recommend having schemas directories structured as follows: 
    ```
      Schemas/all/[YearVersion]/TEGE/
                                    /Common    
                                    /TEGE990
                                    /TEGE990EZ
                                    /TEGE990PF
                                  
    ```

### Technical Details

#### Technical Stack
- Python 3.9 or later
- Pip 21.0 or later
- Virtualenv & Virtualenvwrapper (optional)

#### Python Libraries
- lxml==4.9.3

#### Code Repository Directory Structure

```
Schema Mapper
├── Code   
│   ├── Utils                    
│   │   ├── helpers.py             # Helper functions used by functions by path_generator.py   
│   │   ├── logging.py             # Loggers and logging configuration. 
│   │   ├── path_generator.py.     # Code to process schemas   
│   ├── Main.py                     # Main script that runs the mapper
│   ├── Requirements.txt            # Libraries required for mapper to work. 
│   ├── Settings.py                 # All settings used across project.  
└── Input                           # Where all Schemas to be processed are stored
│   ├── Schemas
│        |──All                     # Contains all schemas by year
│           ├── 2003v2.0            # We are prohibited by IRS from sharing these.
│           ├── 2003v2.1                 
│          .... 
│           ├── 2023v3.0  
├── Logs                            # Logs automatically generated by the mapper 
│   ├── Access.log                  # Log generated when mapper is initated and finished running. 
│   ├── Error-generic.log           # Catches all generic python errors that surface while running the mapper.  
│   ├── Error-nodes.log             # Catches all Node related errors generated while processing schemas
│   ├── Error-schemas.log           # Catches any schema related errors, i.e. schemas missing or wrong folder structure
├── Output                          # Where Data Dictionary is Saved
│   ├── Mapping_[Date].csv          # Final Data Dictionary as csv   
└── Reference_Files                 # Folder containing reference files useful for understanding xmls, schemas, etc
│   └── Blank Form 990:ez:pfs       # Blank Form 990s as PDF
│   │   ├── 990.xml                 # Blank Main Forms 990,990ez,990n, 990pf, 990T
│   │   ├── Schedules               # Blank Schedules as PDFS
│   └── XML Sample Blank Schemas    # Sample Schemas 
│   │   ├── IRS990.xsd              # Sample Form 990 Schema
│   │   ├── IRS990EZ.xsd            # Sample Form 990EZ Schema
│   │   ├── IRS990PF.xsd            # Sample Form 990PF Schema
│   |   ....schedules                         
│   └── XML Sample Returns          # Sample XML Returns
│   │   ├── 990.xsd                 # Sample Form 990 XML - Red Cross
│   │   ├── 990EZ.xsd               # Sample Form 990EZ XML - Little League Baseball
│   │   ├── 990PF.xsd               # Sample Form 990PF XML - Johnson Foundation
│       ....                                                        
└── .gitignore                      # Lists files that will not be committed by git
└── README.md                       # Repo readme file (i..e what you are reading now)
```

### Getting Started

- **Pre-Requirements** 
  - Ensure you have Python 3.9, Pip 21, & Virtualenv installed on your computer.
 
- **Steps:**
  - Clone the github repository 
  - Ensure you have the appropriate data folder structure. If any folders are missing you may get errors. 
    - Look at /input/schemas/all directory & /code/settings.py for the appropriate folder structure & details. 
  - **Optional** If you need to download IRS990 EFile Schemas 
      - You can find the latest schemas via the IRS here -> https://www.irs.gov/pub/irs-schema/
      - You can find a historical compilation of schemas here -> 
  - Create a Python Virtual Environment and install all requirements.txt with pip install -r requirements.txt
  - **Optional** modify settings.py 
    - Change schema folder & files location 
    - You can comment or uncomment specific schmea documents you want parsed. 
  - Activate the virtual environment you created in step 3.
  - Within the code sub-directory run the following:
    ```
    python main.py
    ```
  - Check /output directory for mapping_[date].csv
  - Check log files in /log directory for any potential errors


## FAQ & Troubleshooting -

**Most Common Errors:**
- Misconfigured Code/settings.py
- Missing Schema Directories - Not having the appropriate directory structure in your code base.
  - We recommend having schemas directories structured as follows: 
    ```
      Input/Schemas/all/[YearVersion]/TEGE/
                                    /Common    
                                    /TEGE990
                                    /TEGE990EZ
                                    /TEGE990PF
                                  
    ```
- Missing Schema Files 
- Missing output directory for data dictionary csv to be saved. 

### Acknowledgements 
In 2017 Matt Dragon & David Borenstein at Charity Navigator created a small open source 990 meta data project https://github.com/CharityNavigator/990_metadata/ to map 990xml fields using the IRS Schemas. We at CitizenAudit are indebted to their efforts as we expanded on their library. 

### Licensing TBD
