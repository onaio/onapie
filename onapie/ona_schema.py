class OnaSchemaNode(dict):
    """
    Initialised with form JSON dict. Represents a schema with child fields.

    The JSON dict could be an entire form or just a single field. Implements
    easy field data accessor methods.
    """
    ID_STRING = 'id_string'
    XPATH = 'xpath'
    CHILDREN = 'children'
    TYPE = 'type'
    NAME = 'name'
    LABEL = 'label'

    def __init__(self, schema, parents=None):
        super(OnaSchemaNode, self).__init__(schema)
        parents = parents or []
        xpath = "/".join(parents)
        if len(parents) < 1:
            xpath += "{}"
        else:
            xpath += "/{}"
        self[OnaSchemaNode.XPATH] = xpath.format(self[OnaSchemaNode.NAME])

    def label(self, language=None):
        """
        Return the label for the specified language, or the default language
        if None
        """
        return self.get(OnaSchemaNode.LABEL, self[OnaSchemaNode.NAME])

    def __getattr__(self, item):
        return self[item]


class OnaForm(OnaSchemaNode):
    """
    Subclass of a `OnaSchemaNode` that implements form specific functions
    e.g. default_language

    Example:
    .. code-block:: python

       form = OnaForm({children: [{u'name': u'start', u'type': u'start'} ...]})

       for c in form.children:
           c.label() -> data[c.xpath]
    """
    _fields = {}

    def __init__(self, schema):
        super(OnaForm, self).__init__(schema)
        children = schema[OnaSchemaNode.CHILDREN]
        self._fields = OnaForm._parse_children(children, [])

    @classmethod
    def _parse_children(cls, children, parents=None):
        """
        Flatten the schema and make the fields accessible by xpath
        """
        parents = parents or []
        nodes = {}
        for child in children:
            node = OnaSchemaNode(child, parents)
            nodes[node[OnaSchemaNode.XPATH]] = OnaSchemaNode(
                child, parents)
            if OnaSchemaNode.CHILDREN in node:
                # create a copy of the list
                new_parents = parents[:]
                new_parents.append(node.name)
                child_nodes = cls._parse_children(
                    node[OnaSchemaNode.CHILDREN], new_parents)
                nodes.update(child_nodes)

        return nodes

    def __getitem__(self, xpath):
        """
        Return the field with the specified name
        """
        return self._fields[xpath]