import unittest
import parser
from parserErrors import *
from xml import XML

class testXMLCompare(unittest.TestCase):
    def test_single_tag_same(self):
        tag1 = XML("tag", [])
        tag2 = XML("tag", [])
        self.assertTrue(tag1.compare(tag2))

    def test_single_tag_different(self):
        tag1 = XML("tag", [])
        tag2 = XML("gat", [])
        self.assertFalse(tag1.compare(tag2))

    def test_one_inner_tag_same(self):
        inner1 = XML("inner", [])
        inner2 = XML("inner", [])
        tag1 = XML("tag", [inner1])
        tag2 = XML("tag", [inner2])
        self.assertTrue(tag1.compare(tag2))

    def test_one_inner_tag_different_inner(self):
        inner1 = XML("inner1", [])
        inner2 = XML("inner2", [])
        tag1 = XML("tag", [inner1])
        tag2 = XML("tag", [inner2])
        self.assertFalse(tag1.compare(tag2))

    def test_one_inner_tag_different_outer(self):
        inner1 = XML("inner", [])
        inner2 = XML("inner", [])
        tag1 = XML("tag1", [inner1])
        tag2 = XML("tag2", [inner2])
        self.assertFalse(tag1.compare(tag2))

    def test_two_inner_tags_same(self):
        inner11 = XML("inner1", [])
        inner12 = XML("inner2", [])
        inner21 = XML("inner1", [])
        inner22 = XML("inner2", [])
        tag1 = XML("tag", [inner11, inner12])
        tag2 = XML("tag", [inner21, inner22])
        self.assertTrue(tag1.compare(tag2))

    def test_two_inner_tags_different_order(self):
        inner11 = XML("inner1", [])
        inner12 = XML("inner2", [])
        inner21 = XML("inner1", [])
        inner22 = XML("inner2", [])
        tag1 = XML("tag", [inner12, inner11])
        tag2 = XML("tag", [inner21, inner22])
        self.assertFalse(tag1.compare(tag2))

    def test_multiple_layers_same(self):
        innermost1 = XML("innermost", [])
        innermost2 = XML("innermost", [])
        inside1 = XML("inside", [innermost1])
        inside2 = XML("inside", [innermost2])
        inner1 = XML("inner", [inside1])
        inner2 = XML("inner", [inside2])
        tag1 = XML("tag", [inner1])
        tag2 = XML("tag", [inner2])
        self.assertTrue(tag1.compare(tag2))

    def test_multiple_layers_different_innermost(self):
        innermost1 = XML("innermost1", [])
        innermost2 = XML("innermost2", [])
        inside1 = XML("inside", [innermost1])
        inside2 = XML("inside", [innermost2])
        inner1 = XML("inner", [inside1])
        inner2 = XML("inner", [inside2])
        tag1 = XML("tag", [inner1])
        tag2 = XML("tag", [inner2])
        self.assertFalse(tag1.compare(tag2))

    def test_multiple_layers_different_inside(self):
        innermost1 = XML("innermost", [])
        innermost2 = XML("innermost", [])
        inside1 = XML("inside1", [innermost1])
        inside2 = XML("inside2", [innermost2])
        inner1 = XML("inner", [inside1])
        inner2 = XML("inner", [inside2])
        tag1 = XML("tag", [inner1])
        tag2 = XML("tag", [inner2])
        self.assertFalse(tag1.compare(tag2))

    def test_one_has_inner_tag(self):
        inner = XML("inner", [])
        tag1 = XML("tag", [inner])
        tag2 = XML("tag", [])
        self.assertFalse(tag1.compare(tag2))

    def test_second_has_inner_tag(self):
        inner = XML("inner", [])
        tag1 = XML("tag", [])
        tag2 = XML("tag", [inner])
        self.assertFalse(tag1.compare(tag2))

    def test_missing_one_inner_tag(self):
        inner1 = XML("inner", [])
        inner21 = XML("inner", [])
        inner22 = XML("inner", [])
        tag1 = XML("tag", [inner1])
        tag2 = XML("tag", [inner21, inner22])
        self.assertFalse(tag1.compare(tag2))

    def test_second_missing_one_inner_tag(self):
        inner11 = XML("inner", [])
        inner12 = XML("inner", [])
        inner2 = XML("inner", [])
        tag1 = XML("tag", [inner11, inner12])
        tag2 = XML("tag", [inner2])
        self.assertFalse(tag1.compare(tag2))


class testParser(unittest.TestCase):
    def test_single_tag(self):
        tag = "<tag></tag>"
        result = parser.parseXML(tag)
        match = XML("tag", [])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents, [])
        self.assertTrue(result.compare(match))

    def test_single_tag_with_underscore(self):
        tag = "<_tag></_tag>"
        result = parser.parseXML(tag)
        match = XML("_tag", [])
        self.assertEqual(result.name, "_tag")
        self.assertEqual(result.contents, [])
        self.assertTrue(result.compare(match))

    def test_single_tag_with_period(self):
        tag = "<t.ag></t.ag>"
        result = parser.parseXML(tag)
        match = XML("t.ag", [])
        self.assertEqual(result.name, "t.ag")
        self.assertEqual(result.contents, [])
        self.assertTrue(result.compare(match))

    def test_single_tag_with_dash(self):
        tag = "<t-ag></t-ag>"
        result = parser.parseXML(tag)
        match = XML("t-ag", [])
        self.assertEqual(result.name, "t-ag")
        self.assertEqual(result.contents, [])
        self.assertTrue(result.compare(match))

    def test_single_self_closing_tag(self):
        tag = "<tag />"
        result = parser.parseXML(tag)
        match = XML("tag", [])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents, [])
        self.assertTrue(result.compare(match))

    def test_single_self_closing_tag_without_space(self):
        tag = "<tag/>"
        result = parser.parseXML(tag)
        match = XML("tag", [])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents, [])
        self.assertTrue(result.compare(match))

    def test_document_header(self):
        xml = "<?xml?><tag></tag>"
        result = parser.parseXML(xml)
        match = XML("tag", [])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents, [])
        self.assertTrue(result.compare(match))

    def test_single_inner_tag(self):
        tag = "<tag><inner></inner></tag>"
        result = parser.parseXML(tag)
        inner = XML("inner", [])
        match = XML("tag", [inner])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner")
        self.assertEqual(result.contents[0].contents, [])
        self.assertTrue(result.contents[0].compare(inner))
        self.assertTrue(result.compare(match))

    def test_self_closing_inner_tag(self):
        tag = "<tag><inner /></tag>"
        result = parser.parseXML(tag)
        inner = XML("inner", [])
        match = XML("tag", [inner])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner")
        self.assertEqual(result.contents[0].contents, [])
        self.assertTrue(result.contents[0].compare(inner))
        self.assertTrue(result.compare(match))

    def test_two_inner_tags_different(self):
        tag = "<tag><inner1></inner1><inner2></inner2></tag>"
        result = parser.parseXML(tag)
        inner1 = XML("inner1", [])
        inner2 = XML("inner2", [])
        match = XML("tag", [inner1, inner2])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner1")
        self.assertEqual(result.contents[1].name, "inner2")
        self.assertTrue(result.contents[0].compare(inner1))
        self.assertTrue(result.contents[1].compare(inner2))
        self.assertTrue(result.compare(match))

    def test_two_inner_tags_same(self):
        tag = "<tag><inner></inner><inner></inner></tag>"
        result = parser.parseXML(tag)
        inner1 = XML("inner", [])
        inner2 = XML("inner", [])
        match = XML("tag", [inner1, inner2])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner")
        self.assertEqual(result.contents[1].name, "inner")
        self.assertTrue(result.contents[0].compare(inner1))
        self.assertTrue(result.contents[1].compare(inner2))
        self.assertTrue(result.compare(match))

    def test_two_self_closing_inner_tags(self):
        tag = "<tag><inner1 /><inner2 /></tag>"
        result = parser.parseXML(tag)
        inner1 = XML("inner1", [])
        inner2 = XML("inner2", [])
        match = XML("tag", [inner1, inner2])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner1")
        self.assertEqual(result.contents[1].name, "inner2")
        self.assertTrue(result.contents[0].compare(inner1))
        self.assertTrue(result.contents[1].compare(inner2))
        self.assertTrue(result.compare(match))

    def test_two_inner_first_self_closing(self):
        tag = "<tag><inner1 /><inner2></inner2></tag>"
        result = parser.parseXML(tag)
        inner1 = XML("inner1", [])
        inner2 = XML("inner2", [])
        match = XML("tag", [inner1, inner2])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner1")
        self.assertEqual(result.contents[1].name, "inner2")
        self.assertTrue(result.contents[0].compare(inner1))
        self.assertTrue(result.contents[1].compare(inner2))
        self.assertTrue(result.compare(match))

    def test_two_inner_second_self_closing(self):
        tag = "<tag><inner1></inner1><inner2 /></tag>"
        result = parser.parseXML(tag)
        inner1 = XML("inner1", [])
        inner2 = XML("inner2", [])
        match = XML("tag", [inner1, inner2])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner1")
        self.assertEqual(result.contents[1].name, "inner2")
        self.assertTrue(result.contents[0].compare(inner1))
        self.assertTrue(result.contents[1].compare(inner2))
        self.assertTrue(result.compare(match))

    def test_multiple_layers(self):
        tag = "<tag><inner><inside><innermost></innermost></inside></inner></tag>"
        result = parser.parseXML(tag)
        innermost = XML("innermost", [])
        inside = XML("inside", [innermost])
        inner = XML("inner", [inside])
        match = XML("tag", [inner])
        self.assertEqual(result.name, "tag")
        self.assertEqual(result.contents[0].name, "inner")
        self.assertEqual(result.contents[0].contents[0].name,"inside")
        self.assertEqual(result.contents[0].contents[0].contents[0].name, "innermost")
        self.assertTrue(result.compare(match))
        self.assertTrue(result.contents[0].compare(inner))
        self.assertTrue(result.contents[0].contents[0].compare(inside))
        self.assertTrue(result.contents[0].contents[0].contents[0].compare(innermost))

    def test_empty_string_exception(self):
        self.assertRaises(EmptyInputError, parser.parseXML, "")

    def test_invalid_input_single_tag(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag>")

    def test_invalid_input_no_slash(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag><tag>")

    def test_invalid_input_inner_no_slash(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag><inner></tag>")

    def test_invalid_input_tag_within_tag(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag<inner>></tag>")

    def test_invalid_input_tag_within_selfclose_tag(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag<inner> />")

    def test_invalid_input_xml_tag(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<xml></xml>")

    def test_invalid_input_tag_with_space(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<t ag></t ag>")

    def test_invalid_input_tag_with_special_character(self):
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag@></tag@>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag!></tag!>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<t#ag></t#ag>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<$tag></$tag>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag%></tag%>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag^></tag^>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag&></tag&>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag*></tag*>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag(></tag(>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag)></tag)>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag+></tag+>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag=></tag=>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag[></tag[>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag]></tag]>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag{></tag{>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag}></tag}>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<tag|></tag|>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<\\tag></\\tag>")
        self.assertRaises(InvalidInputError, parser.parseXML, "</tag><//tag>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<>tag></<tag>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<<tag></>tag>")
        self.assertRaises(InvalidInputError, parser.parseXML, "<,tag></,tag>")


if __name__ == "__main__":
    unittest.main()
