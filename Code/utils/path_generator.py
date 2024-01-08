import datetime, os 
import os.path # This module implements some useful functions on pathnames. To read or write files see open(), and for accessing the filesystem see the os module. The path parameters can be passed as either strings, or bytes.
import re # Library used to write regular expressions
import sys # Library gives us access to system 
from lxml import etree # Library used to parse xml 
from .helpers import abbreviate, concat, getByXpath, getRoot, NAMESPACE, nsAdd, remap, resolve, strip  # Grab Helper functions from helpers.py
from .logging import Error_Details, log_node_error

Error_Details.script = os.path.split(sys.argv[0])[1]


# 2 Classes: a Node element and group element. 

class UnhandledElementException(Exception):

    '''
    Input: Exception Type
    Output: 
        1. Writes to Node Log 
        2. Passes -> i.e. does nothing
    '''
    log_node_error(Exception, "! Unhandled Exception: %s" % str(Exception), Error_Details)
    pass

class Node:

    '''

    '''

    def __init__(self, elem, source, version, xpref):
        # Raw fields
        self.elem      = elem
        self.source    = source
        self.version   = version 
        self.xpref     = xpref
        self.apath     = self.ascend(elem)   # Call Ascend function -> gets node and path outputs List containing [Childelement:tag, type, parent] -->['element:Desc', 'sequence', 'complexType:USItemizedEntryType']
        self.namespace = self.getNamespace(self.apath[-1]) # grab last element of list ['element:Desc', 'sequence', 'complexType:USItemizedEntryType'] -> grab 'complexType:USItemizedEntryType'
        self.process() # On creation calls the process function which triggers a variety of functions

    def compose(self, source, prefix, namespace, xpref):

        '''
        Inputs: Source -> Tag, Prefix
        Outputs Node with xpath and namespace
        '''

        #(1) source -> variable tag (2) prefix -> path to tag IRS990ScheduleL/LoansBtwnOrgInterestedPrsnGrp (3) Namespace (4) Xperf -> Return/ReturnData or Return basically telling us which part of xml item is in
        # Source -> IRS990ScheduleL
        # Prefix -> LoansBtwnOrgInterestedPrsnGrp
        # namespace -> IRS990ScheduleLType
        # Xpref -> Return/ReturnData

        # Step 1. Create a node object passing element, tag, version, xpref
        composite = Node(self.elem, source, self.version, xpref)

        # Step 2. add a variable to object called composite xpath which is joining of prefix and xpath with /
        # Example -> GrntAsstBnftInterestedPrsnGrp/BusinessName/BusinessNameLine1Txt
        composite.xpath = "/".join([prefix, self.xpath])

        # Step 3. Set the composite.namespace to namespace
        composite.namespace = namespace
        # Example of a namespace -> IRS990ScheduleLType

        # Step 4. Return the composite
        return composite

    def ascend(self, node, path = []):

        '''
        Input(s): 1. Node 2. Path by default empty list
        Output: List containing [Childelement:tag, type, parent] -->['element:Desc', 'sequence', 'complexType:USItemizedEntryType']

        '''

        # Step 1. Create local variable as a copy of entire path list. Creates a shallow copy
        local = path[:]

        # Step 2. Call abbreviate function store result  -> example output will be complexType:USItemizedEntryType
        abbr = abbreviate(node)

        # Step 3. Check to see if abbreviation is in list "schema"
        if not abbr in ["schema"]:
            # Step 3b. Append to list
            local.append(abbr)

        # Step 4. Get parent
        parent = node.getparent()

        '''
        For example:
            <xsd:complexType name="USItemizedEntryType">  ------- PARENT
                <xsd:sequence>
                    <xsd:element name="Desc" type="LineExplanationType" /> ---- CHILD
                    <xsd:element name="Amt" type="USAmountType" />
                </xsd:sequence>
            </xsd:complexType>

        '''
        # Step 5. Check to see if parent exists
        if parent == None:

            # Step 5b. If parent doesnt exist return local i.e. means you have gotten to end leaf/node of document tree
            # Example of something without parent ['element:Desc', 'sequence', 'complexType:USItemizedEntryType']
            return local

        # Step 6. Else we will call again the same function
        return self.ascend(parent, local)

    def getNamespace(self, token):

        '''
        Input: Token/Node 'complexType:USItemizedEntryType'
        Output: Either namespace 'USItemizedEntryType' or None if Node/Token has no namespace
        '''

        # Step 1. Check to see if token starts with "group"
        if token.startswith("group:"):
            # Step 1b. If it does strip group from token and return as string. 
            return token.split(":")[-1]

        # Step 2. Check to see if token starts with complextype
        if token.startswith("complexType:"):
            # Step 2b. If it does strip complex from token  and return as string-> from 'complexType:USItemizedEntryType' to USItemizedEntryType
            return token.split(":")[-1]

        # Otherwise return non because there is no namespace for this element/node
        return None

    def getAttrib(self, attr):

        '''
        Getting an node/object along with an attribute
        '''

        # Step 1. Search for attribute in xml tree
        if attr in self.elem.attrib:
            # If it's available return attribute
            return self.elem.attrib[attr]

        # Step 2. If can't find return none
        return None

    def getType(self):

        '''
        Function:  gets a type attribue from xml of node object
        ''' 

        # Step 1. Find Inline Type attributes in xml of node object
        # Example -> <xsd:element name="Desc" type="LineExplanationType" />
        if "type" in self.elem.attrib:
            # Step 1b. Return only types 
            return self.elem.attrib["type"]
       
        # Step 2. Check Nested type specifications -- complexType 
        # Complex types often have embedded tags 
        '''

        Example:    
        <xsd:complexType name="USItemizedEntryType">
            <xsd:sequence>
                <xsd:element name="Desc" type="LineExplanationType" />
                <xsd:element name="Amt" type="USAmountType" />
            </xsd:sequence>
        </xsd:complexType>
        '''

        # Step 3. Search object xmml and get list of cplxelements that extend base by calling getbyxpath function passing object and query
        cplxElems = getByXpath(self.elem,"xsd:complexType/*/xsd:extension[@base]")

        # Step 4. Check to see if length of results is > 0 i.e. if there are/is a complex types
        if len(cplxElems) == 1:
            #Step 4b Return attribute base attribute of type
            # example -> EmployeeCompensationExplnType
            return cplxElems[0].attrib["base"]

        # Nested type specification -- simpleType

        # Step 5. Search xml object for simple types where there is a restriction base type
        smplElems = getByXpath(self.elem,"xsd:simpleType/xsd:restriction[@base]")

        # Step 6. Check to see if results > 0 i.e. they exist
        if len(smplElems) == 1:
            # Step 6b. Return the attribute of the base type. 
            # example: TextType
            return smplElems[0].attrib["base"]

        # Step 7. If we can't find any tags then pass an exception
        raise UnhandledElementException("/".join(self.ascend(self.elem)))
    

    def getXpath(self):

        '''
        Function run on Node Class. # Xpath to this node (relative to namespace)

        Input: Results of self.apath and self.namespace
            Exmaple Input: 
            Self.path -> ['element:Sect170c2BPurposeExplnTxt', 'sequence', 'complexType', 'element:DonorAdvisedFundGrp', 'sequence', 'complexType:DonorAdvisedFundStmtType']
            Self.Namespace DonorAdvisedFundStmtType
        Output: xpath -> becomes DonorAdvisedFundGrp/Sect170c2BPurposeExplnTxt
        '''


        # Step 1. Initiate a list/container as variable p
        p = []

        # Step 2. 
        # For Each token in output of Self.Apath -> [Childelement:tag, type, parent] -->['element:Desc', 'sequence', 'complexType:USItemizedEntryType']
        # First tpust list in reverse
        for token in reversed(self.apath):

            # Step 2b. remember self.namespace -> last item in apath list using above example-> 'complexType:USItemizedEntryType' 
            # If self.namespace is not None and : is in token and token ends with self.namespace 'complexType:USItemizedEntryType'
            if (not self.namespace == None) and (":" in token) and\
                    (token.endswith(self.namespace)):
                    # Step 2b1 Then continue
                continue
            # Step 2c If token contains anything in following list 
            if token in ["sequence", "choice", "complexType", "group"]:
                # Step 2c1 continue
                continue
            # Step 2d Take the token and split it on ':' and grab the last part -> 'complexType:USItemizedEntryType' grab -> USItemizedEntryType
            token = token.split(":")[-1]

            # Step 2e then append token to p container
            p.append(token)

        # Step 3. Create an xpath by adding all tokens with / in between

        # Example ['DonorAdvisedFundGrp', 'Sect170c2BPurposeExplnTxt'] -> becomes DonorAdvisedFundGrp/Sect170c2BPurposeExplnTxt
        xp = "/".join(p)

        # Step 4. Return xpath by adding all tokens with / in between
        return "/".join(p)

    def getDescription(self):

        '''
        Function essentially is called by self.process() i.e. at node/object level
        Make call to getUniqueChildText passing argument description
        Output results of getUniqueChild Text

        '''

        return self.getUniqueChildText("Description")

    def getLineNumber(self):

        '''

        Function essentially is called by self.process() i.e. at node/object level
        Make call to getUniqueChildText passing argument LineNumber
        Output results of getUniqueChild Text

        '''
        return self.getUniqueChildText("LineNumber")

    def getUniqueChildText(self, cName):

        '''
        Example of xml traversing:

            <xsd:element name="OtherExpensesGrp" type="Form990PartIXGroup4Type" minOccurs="0" maxOccurs="4">

                <xsd:annotation>

                    <xsd:documentation>

                        <Description>Other expenses</Description>

                        <LineNumber>Part IX Line 24a - 24d</LineNumber>

                    </xsd:documentation>

                </xsd:annotation>

            </xsd:element>


        '''


        # Step 1. Build Xpath Query with information that has been passed # traversing annotation and documentation tags 
        xp = "xsd:annotation/xsd:documentation/%s" % cName

        # Step 2. Call getByXpath function passing an element and query and store results as ds (i.e. will be list of elements)
        ds = getByXpath(self.elem, xp)

        # Step 3. If list is = 0 
        if len(ds) == 0:
            # Step 3b return none
            return None

        # Step 4. If list = 1
        elif len(ds) == 1:
            # Return the text of first element of the ds list
            return ds[0].text
        else:
            # Else raise an assertion error which means the thing we are querying is not unique. 
            raise AssertionError("Expected %s to be unique" % cName)

    def getMin(self):
        '''
        Function: Searches for min occurences
        Input. Node Object 
        Output: 0, None, 1 etc

        Reminder xml looks like this -> <xsd:element name="CountryCd" type="CountryType" minOccurs="0">
        '''

        return self.getAttrib("minOccurs")

    def getMax(self):

        '''
        Function: searches for max occurences
        Input. Node Object 
        Output: 0, None, 1 etc

        Reminder xml looks like this -> <xsd:element name="OtherExpensesGrp" type="Form990PartIXGroup4Type" minOccurs="0" maxOccurs="4">
        '''
        return self.getAttrib("maxOccurs")


    def process(self):
        '''
        Triggers a variety of functions and stores results as variables attachd to node object
        1. Get Type
        2. GetXpath
        3. Get Description
        4. Get Linenumber
        5. Get Min occurences
        6. Get Max occurences
        '''

        # Step 1. Trigger gettype functions and store reults as self.etype 
        self.eType = self.getType()

        # Step 2. Trigger getxpath and store results as self.xpath
        self.xpath = self.getXpath()

        # Step 3. Trigger Get Description and store as self.desc
        self.desc = self.getDescription()

        # Step 4. Trigger linenumber function and store as self.linenum
        self.lineNum = self.getLineNumber()

        # Step 5. Trigger get min and store as self.min
        self.minOccur = self.getMin()

        # Step 6. Trigger get max and store as self.max
        self.maxOccur = self.getMax()


    def examine(self):

        '''
        Function Behavior is that of examining itself 
        Input: runs on Node Class/Object. 

        Output: List including Namespace, path so list [namespace, ['element:Desc', 'sequence', 'complexType:USItemizedEntryType']]

        '''

        return [self.namespace, self.apath] # Return the version of the node's data to be published in the data

    def report(self):

        '''
        Function: run on node class/object

        Input: Node Object
        Output: List of details on node object -> ['2018v1.0', 'IRS990ScheduleD', 'Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt', 'USAmountType', 'Donated services and use of facilities', 'Part XI Line 2b', '0', None]

        '''

        # By the time this code is called, the Xpath should reflect the prefix that was stripped for processing earlier.

        # Step 1. join xpref & xpath with "/" inbetween
            # Xpref -> Return/ReturnData
            # Xpath -> IRS990ScheduleD/DonatedServicesAndUseFcltsAmt
        # Final output -> Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt
        pubXpath = "/".join([self.xpref, self.xpath])

        # Step 2 run a regular expression substituting "/+" with "/ and passing the pubxpath variable"
        pubXpath = re.sub("/+", "/", pubXpath)
        
        # Step 3. Create a list with variables. 
        # Example -> ['2018v1.0', 'IRS990ScheduleD', 'Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt', 'USAmountType', 'Donated services and use of facilities', 'Part XI Line 2b', '0', None]
        ret = [self.version, self.source, pubXpath, self.eType, self.desc, self.lineNum,
                self.minOccur, self.maxOccur]
        

        # Step 4. Call strip function for each variable in ret list (this function ensures they are ascii encoded) and return list
        # Example output -> ['2018v1.0', 'IRS990ScheduleD', 'Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt', 'USAmountType', 'Donated services and use of facilities', 'Part XI Line 2b', '0', None]

        return [strip(x) for x in ret]

class Group(Node):

    '''

    Function: Extends the Node Class and overwrites two functions getType and compose

    '''

    def getType(self):
        # Originally getType function grabs the type explanation <xsd:element name="Desc" type="LineExplanationType" />
        # Now we are looking for the "ref attribute" within the In-line type specifications

        # Step 1 If "ref" is contained in an element attribute  Example ->  <xsd:group ref="Form990PartVIIIMainGroup"/>
        if "ref" in self.elem.attrib:

            # Step 1b. Return Ref attribute
            return self.elem.attrib["ref"]

        # Step 2. Otherwise return an unhandled exception take element call ascend function and join all list with / ['element:Desc', 'sequence', 'complexType:USItemizedEntryType']  
        raise UnhandledElementException("/".join(self.ascend(self.elem)))

    def compose(self, source, prefix, namespace, xpref):

        '''
        This Function run at the group class level
        
        Inputs:
            (1) Source   -> IRS990ScheduleM 
            (2) Prefix   -> ClothingAndHouseholdGoodsGrp
            (3) Namespace -> IRS990ScheduleMType
            (4) xpref -> Return/ReturnData
        Outputs:
            Composite -> Instance of group
            Composite.xpath -> list containing prefix & xpath joined with '/'  -> IRS990ScheduleM/ClothingAndHouseholdGoodsGrp/
            composite.namespace -> namespace   -> IRS990ScheduleMType


        Example: 
            <xsd:element name="ClothingAndHouseholdGoodsGrp" type="Form990SchMGroup2Type" minOccurs="0">

                <xsd:annotation>

                    <xsd:documentation>

                        <Description>Clothing and household goods</Description>

                        <LineNumber>Part I Line 5</LineNumber> 

                    </xsd:documentation>

                </xsd:annotation>

            </xsd:element>



        '''
        # Step 1. Create a composite object -> group object 
        composite = Group(self.elem, source, self.version, xpref)

        # Step 2. Store composite xpath by list containing prefix & xpath joined with '/'  -> IRS990ScheduleM/ClothingAndHouseholdGoodsGrp/
        composite.xpath = "/".join([prefix, self.xpath])

        # Step 3. Set composite.namespace -> as namespace
        composite.namespace = namespace

        # Step 4. Return the composite object
        return composite

def getBaseNamespaces(fn):
    '''

    This function takes a folder path such as: '../schemas/current/2018v1.0'. Looks for the common efile types and
    Returns a dictionary of efile etypes along with nodes. {'IPAddressType': set([<path_generator.Node instance at 0x102ead200>, <path_generator.Node instance at 0x102ead0e0>]), 'ForeignAddressType': set([<path_generator.Node instance at 0x102da2a28>,

    Input: '../schemas/current/2018v1.0'
    Output: Dictionary containing ->  'IPAddressType': set([<path_generator.Node instance at 0x109cb91b8>, <path_generator.Node instance at 0x109cb9170>])

    '''

    # Step 1. store version we are processing: folder path based on / grab only content after third / which represents schema version 2018v1.0
    version = fn.split("/")[3]

    # Step 2. Declare a dictionary called namespaces
    namespaces = {}

    # Step 3. Declare full path where files are we will search i.e. ../schemas/current/2018v1.0/Common/efileTypes.xsd
    # Note EfileTypes.xsd -> is a file which contains base types commonly used across schema files. I.e. standard variables
    path = "%s/Common/efileTypes.xsd" % fn 

    # Step 4. Check to see if the path exist if it doesnt  we return an empty dictionary
    if not os.path.exists(path):
        return namespaces

    # Step 5. Call get root function passing a path name and creates root object and store as root (which is a tree object) as variable root
    root = getRoot(path)

    # Step 6. Store string containing a query that identifies elements with attribute name
    xp = "//xsd:element[@name]"

    #Step 7. Grab elements by calling function getByXpath passing tree/object & path "//xsd:element[@name]"
    # Elemens = list of objects like this -> <Element {http://www.w3.org/2001/XMLSchema}element at 0x102bf5098>
    elems = getByXpath(root, xp)
    
    # Step 8. For each element in element object list. 
    for elem in elems:

        # Step 8b. Try to create a Node Object, with element object, source = None, version = 2018v1.0, xpref = None
        try:
            node = Node(elem, None, version, None)

        # Step 8c. If excepption occurs print that execption occured and continue
        except Exception as e:
            #print ("! Get Base Namespace SKIPPED: %s" % str(e))
            log_node_error(e, "! Get Base Namespace SKIPPED: %s" % str(e), Error_Details)
            continue

        # Step 8d. Call namespace class function which extracts namespace store result as ns... example namespace -> USItemizedEntryType
        ns = node.namespace

        # Step 8e. We want to make sure the node is not empty/none so we assert
        # statement has a condition and if the condition is not satisfied the program will stop and give AssertionError.
        assert node != None

        # Step 8f call nsAdd function passing namespaces dictionary, namespace, and node
        '''
        Example of variables passed
            {}
            USItemizedEntryType
            <path_generator.Node instance at 0x10efa8128>

        Example of output: {'USItemizedEntryType': set([<path_generator.Node instance at 0x108679128>, <path_generator.Node instance at 0x1086791b8>])
        '''
        nsAdd(namespaces, ns, node)
    # Step 9. We return the namespace dictionary
    return namespaces

def process(namespaces, xpref, fn):
    # Set of all element nodes.

    ''' Inputs  
        1. dictionary of basenamespaces i.e. common efile types generated by GetBaseNames Function 
        2. prefix type "Return/ReturnData" or Return
        3. path to file ../schemas/current/2018v1.0/TEGE/Common/Dependencies/GeneralExplanationAttachment.xsd

        Outputs: List of variables -> ['2018v1.0', 'IRS990ScheduleD', 'Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt', 'USAmountType', 'Donated services and use of facilities', 'Part XI Line 2b', '0', None]

    '''

    # Step 1. Create a variable noes that is a python set i.e. data structure. Remember a set is -> A set is a collection which is unordered and unindexed
    nodes = set()

    # Step 2. Set source as path of file and split it based on forward slashes select last one and strip everything after period. 
    # ../schemas/current/2018v1.0/TEGE/Common/Dependencies/GeneralExplanationAttachment.xsd   -> turns into GeneralExplanationAttachment
    source = fn.split("/")[-1].split(".")[0]

    # Step 3. Set Version as path of file  example: ../schemas/current/2018v1.0 - turns into 2018v1.0
    version = fn.split("/")[3]
    
    # Step 4. Call getRoot function (passing file path) creates root object and store as root (which is a tree object) as variable root
    root = getRoot(fn)

    # Step 5. Store string containing a query that identifies elements with attribute name
    xp = "//xsd:element[@name]"

    # Step 6. Create an elements list and populate it by calling GetByXPath function -> passing root object/document and xpathquery i.e. we are going to select all elements that have a naem attribute
    elems = getByXpath(root, xp)

    # Step 7. For each item in list of elements with attribute name
    for elem in elems:

        # Step 7b. Try to create a Node object by passing elmement object, source -> really variable tag, version i.e. schema, and xperf => Return/ReturnData or Return basically telling us which part of xml item is in
        try:
            node = Node(elem, source, version, xpref)
        except Exception as e:
            # Step 7c. If this trial fails create an exception error and continue processing elements
            #print ("!Process Node SKIPPED: %s" % str(e))
            log_node_error(e, "!Process Node SKIPPED: %s" % str(e), Error_Details)
            continue

        # Step 7d. Set NS as the namespace. by calling namespace attribute of Node class example -> complexType:USItemizedEntryType'
        ns = node.namespace 

        # Step 7e. Assert that the node exists if it doesnt stop running remaining code
        assert node != None

        # Step 7f. Call NsAdd function and pass (1) dictionary of basenamespaces i.e. common efile types generated by GetBaseNames Function  (2) ns complexType:USItemizedEntryType' and 3 node element
        nsAdd(namespaces, ns, node)
        # This will generate a dictionary {'USItemizedEntryType': set([<path_generator.Node instance at 0x108679128>, <path_generator.Node instance at 0x1086791b8>]),

        # Step 7g. Add dictionary to the nodes set
        nodes.add(node)

    # Find "group" nodes with "ref" tags

    # Step 8. Create an xpath query for group nodes with "ref tags"
    # If you look at IRS990.xsd you will see tags like this -> <xsd:group ref="Form990PartIXGroup1"/>
    xp = "//xsd:group[@ref]"

    # Step 9. Create an elements list and populate it by calling GetByXPath function -> passing root object/document and xpathquery i.e. we are going to select all elements that have a ref attribute
    elems = getByXpath(root, xp)

    # Step 10 For each element in list of elems with a ref attribute
    for elem in elems:

        # Step 10b1. Try to create a Group node by passing (1) element object (2) source -> variable tag (3) version -> schema -> (4) Return/ReturnData or Return basically telling us which part of xml item is in
        try:
            group = Group(elem, source, version, xpref)

        # Step 10b2 If error print exception and skip
        except Exception as e:
            #print ("Process Group !SKIPPED: %s" % str(e))
            log_node_error(e, "Process Group !SKIPPED: %s" % str(e), Error_Details)
            continue
        
        # Step 10c. Set Ns as the namespace by calling namespace attribute of group class example -> Form990PartIXGroup2Typee'
        ns = group.namespace 

        # Step 10d Assert that group is not none
        assert group != None

        # Step 10e. Call NsAdd function and pass (1) dictionary of basenamespaces i.e. common efile types generated by GetBaseNames Function  (2) ns complexType:USItemizedEntryType' and 3 node element
        nsAdd(namespaces, ns, group)

        # Step 10f. Add dictionary to the nodes set
        nodes.add(group)

    # Step 11. Call remap passing nodes and namespaces and store resulting nodes as nodes
    nodes = remap(nodes, namespaces)

    # Step 12. For each n in namespaces where key is "none" run the report class function and store results as lines
    lines = [n.report() for n in namespaces[None]]

    # Step 13. Return Lines i.e. list of reports - [ ['2018v1.0', 'IRS990ScheduleD', 'Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt', 'USAmountType', 'Donated services and use of facilities', 'Part XI Line 2b', '0', None]]
    return lines
