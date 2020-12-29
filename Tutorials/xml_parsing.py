import xml.etree.ElementTree as ET



#Each element has a number of properties associated with it:
#1) a tag which is a string identifying what kind of data this element represents (the element type, in other words).
#2) a number of attributes, stored in a Python dictionary.
#3) a text string.
#4) an optional tail string.
#5) a number of child elements, stored in a Python sequence


xml_file_path="data/movies.xml"
tree=ET.parse(xml_file_path)
root=tree.getroot()
print("root is" ,root.tag)

print("------------------------------------------------")

print("root attributes", root.attrib)

print("------------------------------------------------")

print("root direct children are:")

for child in root:
    print(child.tag, child.attrib)

print("------------------------------------------------")

print("iterating over elements root.iter():")
[print(elem.tag) for elem in root.iter()]
print("------------------------------------------------")

print("printing the xml doc: ")
print(ET.tostring(root,encoding='utf8').decode('utf8'))

print("------------------------------------------------")

#Supported XPath syntax

#tag                    Selects all child elements with the given tag. For example, spam selects all child elements named spam, and spam/egg selects all grandchildren named egg in all children named spam.
#*                      Selects all child elements. For example, */egg selects all grandchildren named egg.
#.                      Selects the current node. This is mostly useful at the beginning of the path, to indicate that it’s a relative path.
#//                     Selects all subelements, on all levels beneath the current element. For example, .//egg selects all egg elements in the entire tree.
#..                     Selects the parent element.
#[@attrib]              Selects all elements that have the given attribute.
#[@attrib='value']      Selects all elements for which the given attribute has the given value. The value cannot contain quotes.
#[tag]                  Selects all elements that have a child named tag. Only immediate children are supported.
#[tag='text']           Selects all elements that have a child named tag whose complete text content, including descendants, equals the given text.
#[position]             Selects all elements that are located at the given position. The position can be either an integer (1 is the first position), the expression last() (for the last position), or a position relative to the last position (e.g. last()-1).

nodes=tree.getroot().find("./genre/decade/[@years='1980s']")
[print(elem.tag) for elem in nodes.iter()]



year=tree.getroot().find("./genre/decade/movie/year")
year.text=str( int(year.text) + 1)
print(year.text)
#tree.write("data/output.xml")