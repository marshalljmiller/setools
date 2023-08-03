# Copyright 2016, Tresys Technology, LLC
#
# SPDX-License-Identifier: LGPL-2.1-only
#
#
from PyQt5 import QtCore
import setools

from .. import details
from . import modelroles
from .table import SEToolsTableModel


class TypeTable(SEToolsTableModel[setools.Type]):

    """Table-based model for types."""

    headers = ["Name", "Attributes", "Aliases", "Permissive"]

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole):
        if not self.item_list or not index.isValid():
            return None

        row = index.row()
        col = index.column()
        item = self.item_list[row]

        match role:
            case QtCore.Qt.ItemDataRole.DisplayRole:
                match col:
                    case 0:
                        return item.name
                    case 1:
                        return ", ".join(sorted(a.name for a in item.attributes()))
                    case 2:
                        return ", ".join(sorted(a for a in item.aliases()))
                    case 3:
                        return "Permissive" if item.ispermissive else None

            case modelroles.ContextMenuRole:
                if col == 1:
                    return (details.typeattr_detail_action(ta) for ta in sorted(item.attributes()))

            case QtCore.Qt.ItemDataRole.WhatsThisRole:
                match col:
                    case 0:
                        column_whatsthis = "<p>This is the name of the type.</p>"
                    case 1:
                        column_whatsthis = \
                            "<p>This is the list of attributes this type belongs to.</p>"
                    case 2:
                        column_whatsthis = \
                            "<p>This is the list of alias names for this type.</p>"
                    case 3:
                        column_whatsthis = \
                            "<p>This indicates whether the type is permissive.</p>"
                    case _:
                        column_whatsthis = ""

                return \
                    f"""
                    <b><p>Table Representation of SELinux Types</p></b>

                    <p>Each part of the declaration is represented as a column in the table.</p>

                    {column_whatsthis}
                    """

        return super().data(index, role)
