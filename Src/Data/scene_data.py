import maya.cmds as cmd
import maya.mel as mel


class SceneData(object):

    @staticmethod
    def load_scene_data(node_name, node_attr):
        """
        Loads the data stored in the scene nodes.
        :param str node_name: Name of the node.
        :param str node_attr: Name of the node's attribute.
        :return: Stored value.
        :rtype: str
        """
        SceneData.create_node(node_name)
        SceneData.add_attr(node_name, node_attr)
        return SceneData.get_node_attr_value(node_name, node_attr)

    @staticmethod
    def save_scene_data(node_name, node_attr, attr_value):
        """
        Saves the specified data in a scene node.
        :param str node_name: Name of the node.
        :param str node_attr: Name of the node's attribute.
        :param str attr_value: Value to be stored.
        """
        SceneData.create_node(node_name)
        SceneData.add_attr(node_name, node_attr)
        SceneData.set_node_attr_value(node_name, node_attr, attr_value)

    @staticmethod
    def create_node(node_name, node_type='dagContainer'):
        """
        Creates a new node.
        :param str node_name: Name of the node.
        :param str node_type: Node type.
        """
        nodes = node_name.split('|')

        for i, node in enumerate(nodes):
            if not cmd.objExists(node):
                if i == 0:
                    cmd.createNode(node_type, n=node, p=None)
                else:
                    cmd.createNode(node_type, n=node, p=nodes[i-1])

    @staticmethod
    def delete_node(node_name):
        """
        Deletes a existing node.
        :param str node_name: Name of the node.
        """
        if cmd.objExists(node_name):
            cmd.delete(node_name)

    @staticmethod
    def add_attr(node_name, attr_name, attr_type='string'):
        """
        Adds a new attribute to the specified node.
        :param str node_name: Name of the node.
        :param str attr_name: Name of the node's attribute.
        :param str attr_type:Attribute type.
        """
        full_attr_name = '{0}.{1}'.format(node_name, attr_name)
        if not cmd.objExists(full_attr_name):
            cmd.addAttr(node_name, longName=attr_name, dataType=attr_type)

    @staticmethod
    def delete_attr(node_name, attr_name):
        """
        Deletes an attribute from the specified node.
        :param str node_name: Name of the node.
        :param str attr_name: Name of the node's attribute.
        """
        full_attr_name = '{0}.{1}'.format(node_name, attr_name)
        if cmd.objExists(full_attr_name):
            cmd.deleteAttr(n=node_name, attribute=attr_name)

    @staticmethod
    def get_node_attr_value(node_name, attr_name):
        """
        Gets the value of a specified node attribute.
        :param str node_name: Name of the node.
        :param str attr_name: Name of the node's attribute.
        """
        full_attr_name = '{0}.{1}'.format(node_name, attr_name)
        SceneData.unlock_node_attr(node_name, attr_name)
        attr_value = cmd.getAttr(full_attr_name)
        SceneData.lock_node_attr(node_name, attr_name)
        return str(attr_value or '')

    @staticmethod
    def set_node_attr_value(node_name, attr_name, attr_value, attr_type='string'):
        """
        Sets the value of a specified node attribute.
        :param str node_name: Name of the node.
        :param str attr_name: Name of the node's attribute.
        :param str attr_value: Value of the node's attribute.
        :param str attr_type: Attribute type.
        """
        full_attr_name = '{0}.{1}'.format(node_name, attr_name)
        SceneData.unlock_node_attr(node_name, attr_name)
        cmd.setAttr(full_attr_name, attr_value, type=attr_type)
        SceneData.lock_node_attr(node_name, attr_name)

    @staticmethod
    def lock_node_attr(node_name, attr_name):
        """
        Locks a specified node attribute.
        :param str node_name: Name of the node.
        :param str attr_name: Name of the node's attribute.
        """
        full_attr_name = '{0}.{1}'.format(node_name, attr_name)
        cmd.setAttr(full_attr_name, lock=True)

    @staticmethod
    def unlock_node_attr(node_name, attr_name):
        """
        Unlocks a specified node attribute.
        :param str node_name: Name of the node.
        :param str attr_name: Name of the node's attribute.
        """
        full_attr_name = '{0}.{1}'.format(node_name, attr_name)
        cmd.setAttr(full_attr_name, lock=False)

