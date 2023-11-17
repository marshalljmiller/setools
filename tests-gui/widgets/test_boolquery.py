# SPDX-License-Identifier: GPL-2.0-only
import typing

from PyQt6 import QtWidgets
import pytest
from pytestqt.qtbot import QtBot

import setools
from setoolsgui.widgets.boolquery import BoolQueryTab


@pytest.fixture
def widget(mock_policy, request: pytest.FixtureRequest, qtbot: QtBot) -> BoolQueryTab:
    """Pytest fixture to set up the widget."""
    marker = request.node.get_closest_marker("obj_args")
    kwargs = marker.kwargs if marker else {}
    w = BoolQueryTab(mock_policy, None, **kwargs)
    qtbot.addWidget(w)
    w.show()
    return w


def test_docs(widget: BoolQueryTab) -> None:
    """Check that docs are provided for the widget."""
    assert widget.whatsThis()
    assert widget.table_results.whatsThis()
    assert widget.raw_results.whatsThis()

    for w in widget.criteria:
        assert w.toolTip()
        assert w.whatsThis()

    results = typing.cast(QtWidgets.QTabWidget, widget.results)
    for index in range(results.count()):
        assert results.tabWhatsThis(index)


def test_layout(widget: BoolQueryTab) -> None:
    """Test the layout of the criteria frame."""
    name, state = widget.criteria

    assert widget.criteria_frame_layout.columnCount() == 2
    assert widget.criteria_frame_layout.rowCount() == 2
    assert widget.criteria_frame_layout.itemAtPosition(0, 0).widget() == name
    assert widget.criteria_frame_layout.itemAtPosition(0, 1).widget() == state
    assert widget.criteria_frame_layout.itemAtPosition(1, 0).widget() == widget.buttonBox
    assert widget.criteria_frame_layout.itemAtPosition(1, 1).widget() == widget.buttonBox


def test_criteria_mapping(widget: BoolQueryTab) -> None:
    """Test that widgets save to the correct query fields."""
    name, state = widget.criteria

    assert isinstance(widget.query, setools.BoolQuery)
    assert name.attrname == "name"
    assert state.attrname == "default"
