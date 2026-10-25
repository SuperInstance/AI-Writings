"""Tests for tools/story_checker.py — story validation utilities."""

import os
import sys
import pytest

# Make story_checker importable from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from story_checker import (
    Frontmatter,
    StoryReport,
    check_consistency,
    extract_character_names,
    extract_title,
    parse_frontmatter,
    validate_story,
    word_count,
)


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

class TestParseFrontmatter:
    def test_no_frontmatter(self):
        text = "# Hello\n\nSome text.\n"
        fm, body = parse_frontmatter(text)
        assert not fm.present
        assert "# Hello" in body

    def test_basic_frontmatter(self):
        text = "---\ntitle: My Story\nauthor: Test\n---\n\n# My Story\n\nBody text.\n"
        fm, body = parse_frontmatter(text)
        assert fm.present
        assert fm.fields["title"] == "My Story"
        assert fm.fields["author"] == "Test"
        assert "# My Story" in body

    def test_frontmatter_with_extra_whitespace(self):
        text = "\n---\n  title:  Spaces  \n---\n# Title\n"
        fm, body = parse_frontmatter(text)
        assert fm.present
        assert fm.fields["title"] == "Spaces"

    def test_empty_frontmatter(self):
        text = "---\n---\n# Title\n"
        fm, body = parse_frontmatter(text)
        # Empty frontmatter block is recognized but has no fields
        assert fm.present
        assert fm.fields == {}
        assert "# Title" in body

    def test_unclosed_frontmatter(self):
        """If opening --- has no closing ---, treat as no frontmatter."""
        text = "---\ntitle: Oops\n# Title\n"
        fm, body = parse_frontmatter(text)
        assert not fm.present


# ---------------------------------------------------------------------------
# Title extraction
# ---------------------------------------------------------------------------

class TestExtractTitle:
    def test_atx_h1(self):
        assert extract_title("# My Story\n\nParagraph.") == "My Story"

    def test_atx_h1_with_formatting(self):
        assert extract_title("# **Bold Title**") == "**Bold Title**"

    def test_setext_title(self):
        text = "My Story\n========\n\nParagraph."
        assert extract_title(text) == "My Story"

    def test_no_title(self):
        assert extract_title("Just some text.\n\nNo heading here.") is None

    def test_h2_not_title(self):
        assert extract_title("## Subtitle\n\nText.") is None

    def test_first_h1_wins(self):
        text = "# First\n\n# Second\n"
        assert extract_title(text) == "First"


# ---------------------------------------------------------------------------
# Word count
# ---------------------------------------------------------------------------

class TestWordCount:
    def test_simple(self):
        assert word_count("hello world") == 2

    def test_strips_code_blocks(self):
        text = "before\n```python\nprint('hi')\n```\nafter"
        # "before" + "after" = 2
        assert word_count(text) == 2

    def test_strips_links_keeps_text(self):
        assert word_count("[click here](http://example.com)") == 2

    def test_strips_images(self):
        # Image alt text remains after stripping image syntax
        assert word_count("![alt](img.png)") == 1

    def test_markdown_formatting(self):
        # Bold/italic markers stripped; "bold", "and", "italic" remain
        assert word_count("**bold** and *italic*") == 3

    def test_empty(self):
        assert word_count("") == 0


# ---------------------------------------------------------------------------
# Character name extraction
# ---------------------------------------------------------------------------

class TestExtractCharacterNames:
    def test_basic_names(self):
        text = "Amara walked in. Amara sat down. Kwame arrived. Kwame nodded."
        names = extract_character_names(text)
        assert "Amara" in names
        assert "Kwame" in names

    def test_single_mention_excluded(self):
        """Names must appear 2+ times."""
        text = "Eleanor walked into the room. She never appeared again."
        names = extract_character_names(text)
        assert "Eleanor" not in names

    def test_stop_words_filtered(self):
        text = "The The The She She She There There There"
        names = extract_character_names(text)
        assert "The" not in names

    def test_mixed_case_sensitivity(self):
        """Each capitalized form is tracked independently."""
        text = "Amara said. Amara nodded. amara doesn't count."
        names = extract_character_names(text)
        assert "Amara" in names


# ---------------------------------------------------------------------------
# Story validation
# ---------------------------------------------------------------------------

class TestValidateStory:
    def _make_story(self, body: str) -> str:
        return f"# Test Story\n\n{body}"

    def test_valid_story(self):
        text = self._make_story("Enough words here to be a real story. " * 10)
        report = validate_story("test.md", text)
        assert report.ok
        assert report.title == "Test Story"
        assert report.word_count > 0

    def test_missing_title(self):
        report = validate_story("notitle.md", "Just some text without a heading.")
        assert not report.ok
        assert any("No title" in e for e in report.errors)

    def test_min_words(self):
        report = validate_story("short.md", "# Short\n\nHi.", min_words=100)
        assert not report.ok
        assert any("below minimum" in e for e in report.errors)

    def test_max_words(self):
        long_body = "word " * 1000
        report = validate_story("long.md", f"# Long\n\n{long_body}", max_words=100)
        assert not report.ok
        assert any("exceeds maximum" in e for e in report.errors)

    def test_no_require_title(self):
        report = validate_story("notitle.md", "No heading.", require_title=False)
        assert report.ok

    def test_require_frontmatter(self):
        report = validate_story("nofm.md", "# Title\n\nBody.", require_frontmatter=True)
        assert any("No frontmatter" in w for w in report.warnings)

    def test_character_names_extracted(self):
        text = "# Cast\n\nElena ran. Elena jumped. Marcus walked. Marcus talked."
        report = validate_story("cast.md", text)
        assert "Elena" in report.character_names
        assert "Marcus" in report.character_names


# ---------------------------------------------------------------------------
# Consistency checks
# ---------------------------------------------------------------------------

class TestCheckConsistency:
    def test_recurring_character(self):
        r1 = StoryReport(path="a.md", character_names=["Elena", "Marcus"])
        r2 = StoryReport(path="b.md", character_names=["Elena"])
        r3 = StoryReport(path="c.md", character_names=["Elena", "David"])
        warnings = check_consistency([r1, r2, r3])
        assert any("Elena" in w and "3 files" in w for w in warnings)

    def test_no_recurring(self):
        r1 = StoryReport(path="a.md", character_names=["Alice"])
        r2 = StoryReport(path="b.md", character_names=["Bob"])
        warnings = check_consistency([r1, r2])
        assert len(warnings) == 0


# ---------------------------------------------------------------------------
# StoryReport
# ---------------------------------------------------------------------------

class TestStoryReport:
    def test_ok_when_no_errors(self):
        r = StoryReport(path="test.md")
        assert r.ok

    def test_not_ok_with_errors(self):
        r = StoryReport(path="test.md", errors=["bad"])
        assert not r.ok

    def test_str_includes_path(self):
        r = StoryReport(path="my-story.md")
        assert "my-story.md" in str(r)
