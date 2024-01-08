from lxml import etree # Library used to parse xml 
import re # Library used to write regular expressions

# Helper functions which are used by Path_Generator.py 
NAMESPACE = {'xsd':'http://www.w3.org/2001/XMLSchema'}  # Top level namespace in XML

def strip(s):
    '''
    Helper Function

    Inputting an object/string/etc
    Outputting object encoded in ascii  
    '''

    # Step 1. Check if string = None
    if s == None:
        # Step 1b. If none return None
        return None

    # Step 2. Return object encoded in ascii
    return s.encode("ascii", "ignore")

# Returns root of etree for which default namespaces have been removed.
# Adapted from Stack Overflow 34009992.

def getRoot(fn):
    '''

    Helper Function: 

    Input:  path -> ../schemas/current/2018v1.0/Common/efileTypes.xsd
    Output: get root object as an xml tree

    '''
    # Step 1. Open xml file given path and store it as a string
    with open(fn) as f:
        xmlstring = f.read().encode()

    xmlstring = xmlstring.decode("utf-8")
    # Step 2. Run a regular expression re.sub(pattern, repl, string, count=0, flags=0);
    # This regular expresion replaces substrings the pattern is to search for xmlns and strip it

    '''

    <?xml version="1.0" encoding="UTF-8"?>
    <xsd:schema targetNamespace="http://www.irs.gov/efile" xmlns="http://www.irs.gov/efile"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
     elementFormDefault="qualified" attributeFormDefault="unqualified" version="1.0">

    <?xml version="1.0" encoding="UTF-8"?>
    <xsd:schema targetNamespace="http://www.irs.gov/efile" (STRIPPED)
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    elementFormDefault="qualified" attributeFormDefault="unqualified" version="1.0">

    '''
    xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
    
    # Step 3. Parse the now stripped string and store as an xml tree object
    root = etree.fromstring(xmlstring.encode()) 

    # Step 4. Return this tree object
    return root

def getByXpath(elem, xp):
    '''
    Helper Function:

    Inputs: (1) an element tree object (2) xpath query "//xsd:element[@name]"  @ = attribute so select attribute = name essentially second input suggest to find all elements with attribute called name
    Output: list of element objects <Element {http://www.w3.org/2001/XMLSchema}element at 0x102bf5098>

    '''
    #  calling xpath query method from lxml performs a global XPath query against the document. 
    # xp is the path we are searching for and namespace is root {'xsd':'http://www.w3.org/2001/XMLSchema'}
    # Namespace is the namespace of document which is used increating an expath query
    # Decent primer on xpaths -> https://docs.oracle.com/cd/B10501_01/appdev.920/a96620/appcxpa.htm
    return elem.xpath(xp, namespaces=NAMESPACE)


def nsAdd(tbl, key, content):
    '''
    Helper Function: 

    Function takes namespace dictionary, namespace, node.... parent with children 
    Input Example of variables passed in 
            Namespaces emtpy dictionary: {}
            Namespace: USItemizedEntryType
        Node: <path_generator.Node instance at 0x10efa8128>

    Output: output: {'USItemizedEntryType': set([<path_generator.Node instance at 0x108679128>, <path_generator.Node instance at 0x1086791b8>]), in this case we have a parent with two nodes
    '''

    # Step 1. If namespace is not a key in the empty dictionary 
    if not key in tbl:
        # Step 1b. Store namespace into the empty dictionary as a key and set the value as empty set -> A set is a collection which is unordered and unindexed
        tbl[key] = set() # result will be -> {'USItemizedEntryType': set([])}

    # Step 2. Assert that node we will add is not None if so stop running and throw assertion error
    assert content != None

    # Step 3. Now that there is no error add the node/content to the dictionary output: {'USItemizedEntryType': set([<path_generator.Node instance at 0x108679128>, <path_generator.Node instance at 0x1086791b8>]), in this case we have a parent with two nodes
    tbl[key].add(content)

def concat(prefix, child):

    '''
    Helper Function
    
    Inputs:
        Prefix: 
        Child: 
    Outputs: 

    '''
    # Step 1. Call ascend method passing child set results as path -> ['element:Desc', 'sequence', 'complexType:USItemizedEntryType']
    path = ascend(child)

    # Step 2. Grab second item in path and put /sequence
    suffix = "/".join(path[1:])

    # Step 3. Create list and store prefix, suffix in it -> prefix could be something like LoansBtwnOrgInterestedPrsnGrp
    units = [prefix, suffix]

    #Step 4. return contactenated string /LoansBtwnOrgInterestedPrsnGrp/sequence or return/return990/LoansBtwnOrgInterestedPrsnGrp/
    return "/".join(units)

def resolve(elem):

    '''
    Helper Function

    Input: Element
    Purpose: Calls either a remapping or report of element after getting the etype

    '''

    # Step 1. Call Get Get Type Method and store results as elem -> This method gets a type attribue from xml of node object
    eType = getType(elem)

    # Step 2. Check to see if etype is in namespaces -> remember namespaces are created by method -> getBaseNamespaces which is a dictionary of lables with objects -> 'IPAddressType': set([<path_generator.Node instance at 0x109cb91b8>, <path_generator.Node instance at 0x109cb9170>])
    if eType in namespaces:

        # Step 2b. Call remap helper function passing the element, along with the value of etype in the namespaces dictionary which will be a set of objects
        remap(elem, namespaces[eType])

    # Step 3. If the etype is not in namespaces 
    else:
        # Step 3b. Call the report class method (which generates a repote of variable ) ->['2018v1.0', 'IRS990ScheduleD', 'Return/ReturnData/IRS990ScheduleD/DonatedServicesAndUseFcltsAmt', 'USAmountType', 'Donated services and use of facilities', 'Part XI Line 2b', '0', None] 
        report(elem)

def abbreviate(node):

    '''
    Helper Function

    Purpose of this function is to take a node element and to create a string with the type:name i.e. abbreviation for it
    Input: Node Element
    Output: String with Type:Name
    '''
    #Step 1. Run Regular Expression Escape which returns ->  Return string with all non-alphanumerics backslashed; this is useful if you want to match an arbitrary literal string that may have regular expression metacharacters in it.
    ns = re.escape("{http://www.w3.org/2001/XMLSchema}")
    # So output will be "\{http\:\/\/www\.w3\.org\/2001\/XMLSchema\}"

    #Step 2. Currently the node tag will be -> {http://www.w3.org/2001/XMLSchema}sequence we want only last part -> sequence
    # Run a regular expression that replaces everything in ns with empty string
    # re.sub(pattern, repl, string input, count=0, flags=0);
    tag = re.sub(ns, "", node.tag)


    # Step 3. Store tag inside a list called ret
    ret = [tag]

    # Step 4. Check to see if node has an attribute called "name" <xsd:simpleType name="FUTAStateCdType">
    if "name" in node.attrib:                                                                # Tag          # Name
        # Step 4b. Append the name to the list that already contains tag. result will be -> ['complexType', 'USItemizedEntryType']
        ret.append(node.attrib["name"])
    
    # Step 5. Join all elements in string with : in between and return them
    # Example Turn -> ['complexType', 'USItemizedEntryType'] into ->  complexType:USItemizedEntryType
    return ":".join(ret)

def remap(nodes, namespaces):

    '''
    Helper function

    Inputs:
        Nodes 
        Name Spaces

    Outputs: Returns a local copy of nodes after having been processed 

    '''

    # Step 1. create a local shallow copy of nodes object
    local = nodes.copy()

    # Step 2. While True
    while True:

        # Step 2b. Create a copy of local and set it as current
        current = local.copy()

        # Step 2c. for each eitm in current copy
        for node in current:

            # Step 2c2 . Set t as the node.eType -> remember etype is set in process method of node
            t = node.eType

            # Step 2c3 Set ns as node.namespace
            ns = node.namespace

            # Step 2c4. If t is not none and t is in the keys of namespaces dictionary
            if t != None and t in namespaces.keys():

                # Step 2c4b. Set prefix as node.xpath
                prefix = node.xpath

                # Step 2c4c. Remove node from list of nodes in local
                local.remove(node)

                # Step 2c4d. Remove node from the set inside the namespaces dictionary
                namespaces[ns].remove(node)

                # Step 2c4e. For each child in the namespaces dictionary set
                for child in namespaces[t]:

                    # Step 2c4e2 Set composite by calling compose method 
                    composite = child.compose(node.source, prefix, ns, node.xpref)

                    # Step 2c4e3 Assert that composite is not none
                    assert composite != None

                    # Step 2c4e4 Add the composite node to the namespacesdictionary
                    namespaces[ns].add(composite)

                    # Step 2c4e5 Add composite to the list of local nodes
                    local.add(composite)

        # Step 2d if Local copy is unchanged 
        if len(local.difference(current)) == 0:

            # Step 2d2 Break then break because it means it has been unchanged. 
            break

        # Step 2e Set current = local 
        current = local

    # Step 3. Return Local
    return local 