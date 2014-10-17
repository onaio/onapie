import unittest

from onapie.ona_schema import OnaSchemaNode, OnaForm


class TestOnaSchemaNode(unittest.TestCase):
    def test_sets_xpath_to_name_if_parents_is_none(self):
        node = OnaSchemaNode({OnaSchemaNode.NAME: 'age'})
        self.assertEqual(node[OnaSchemaNode.XPATH], 'age')

    def test_computes_xpath_if_len_parents_gt_one(self):
        node = OnaSchemaNode(
            {OnaSchemaNode.NAME: 'age'}, ['test', 'group', 'schema'])
        self.assertEqual(node[OnaSchemaNode.XPATH], 'test/group/schema/age')

    def test_get_label_without_language(self):
        node = OnaSchemaNode({
            OnaSchemaNode.NAME: 'age',
            OnaSchemaNode.LABEL: "Age"
        })
        label = node.label()
        self.assertEqual(label, "Age")


class TestOnaForm(unittest.TestCase):
    def test_parse_children(self):
        schema = {
            OnaSchemaNode.ID_STRING: 'personnel_form',
            OnaSchemaNode.CHILDREN: [
                {
                    OnaSchemaNode.NAME: 'personal_details',
                    OnaSchemaNode.LABEL: u"Personal Details",
                    OnaSchemaNode.TYPE: 'group',
                    OnaSchemaNode.CHILDREN: [
                        {
                            OnaSchemaNode.NAME: 'first_name',
                            OnaSchemaNode.LABEL: u"First Name",
                        },
                        {
                            OnaSchemaNode.NAME: 'last_name',
                            OnaSchemaNode.LABEL: u"Last Name",
                        }
                    ]
                }
            ]
        }
        nodes = OnaForm._parse_children(schema[OnaSchemaNode.CHILDREN])
        self.assertEqual(sorted(nodes.keys()), sorted([
            'personal_details',
            'personal_details/first_name',
            'personal_details/last_name',
        ]))
