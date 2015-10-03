from __future__ import unicode_literals
import pytest
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document

@pytest.fixture
def completer():
    from cycli.completer import CypherCompleter
    return CypherCompleter(
        labels=["Movie", "Person"],
        relationship_types=["ACTED_IN", "DIRECTED"],
        properties=["name", "title"]
    )

@pytest.fixture
def complete_event():
    from mock import Mock
    return Mock()

def test_empty_string_completion(completer, complete_event):
    text = ""
    position = 0

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == []

def test_label_completion(completer, complete_event):
    text = "MATCH (p:P"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == [Completion(text="Person", start_position=-1)]

def test_rel_completion(completer, complete_event):
    text = "MATCH (p:Person)-[:A"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == [Completion(text="ACTED_IN", start_position=-1)]

def test_label_completion_after_rel(completer, complete_event):
    text = "MATCH (p:Person)-[:ACTED_IN]->(m:M"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == [Completion(text="Movie", start_position=-1)]

def test_property_completion(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.n"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == [Completion(text="name", start_position=-1)]

def test_no_completions_while_inside_string(completer, complete_event):
    text = "MATCH (p:Person) WHERE p.name = 'Tom H"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == []

def test_match_keyword_completion(completer, complete_event):
    text = "MAT"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == [Completion(text="MATCH", start_position=-3)]

def test_nested_function_completion(completer, complete_event):
    text = "MATCH n RETURN LENGTH(COL"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result == [Completion(text="COLLECT", start_position=-3)]

def test_markov_w_after_match(completer, complete_event):
    # Out of the words starting with W, WHERE is most commonly used after MATCH.
    text = "MATCH n W"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result[0] == Completion(text="WHERE", start_position=-1)

def test_markov_w_after_case(completer, complete_event):
    # Out of the words starting with W, WHEN is most commonly used after CASE.
    text = "MATCH n RETURN CASE W"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result[0] == Completion(text="WHEN", start_position=-1)

def test_markov_w_after_nothing(completer, complete_event):
    # Out of the words starting with W, WITH is most commonly the first word in a query.
    text = "W"
    position = len(text)

    result = list(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))

    assert result[0] == Completion(text="WITH", start_position=-1)
