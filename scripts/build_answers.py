#!/usr/bin/env python3
"""Build report.md, answers.json, and qa/question-map.json from structured answers."""
import argparse
import json
import re
import sys
from pathlib import Path


def validate_answer(text, label):
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"{label}: must be a non-empty string")
    # Formula regions are opaque: preserve their contents exactly, while checking delimiters.
    prose = []
    i = 0
    while i < len(text):
        if text[i] == '$':
            if i + 1 < len(text) and text[i + 1] == '$':
                raise ValueError(f"{label}: display math $$ is not allowed")
            end = text.find('$', i + 1)
            if end < 0:
                raise ValueError(f"{label}: unmatched formula delimiter '$'")
            if end == i + 1 or not text[i + 1:end].strip():
                raise ValueError(f"{label}: empty formula is not allowed")
            i = end + 1
        else:
            prose.append(text[i])
            i += 1
    outside = ''.join(prose)
    if '\n' in ''.join(re.findall(r'\$([^$]*)\$', text)):
        raise ValueError(f"{label}: formulas must use single-line inline $...$ syntax")
    forbidden = [
        (r'(?m)^\s{0,3}#{1,6}(?:\s|$)', 'Markdown headings'),
        (r'(?m)^\s{0,3}(?:```|~~~)', 'code fences'),
        (r'(?m)^\s*\|.*\|\s*$', 'Markdown tables'),
        (r'!\[[^\]]*\]\([^)]*\)', 'Markdown images'),
        (r'\[[^\]]*\]\([^)]*\)', 'Markdown links'),
        (r'\*\*|__|~~|`', 'Markdown emphasis or inline code'),
        (r'(?<!\*)\*[^*\n]+\*(?!\*)|(?<!_)_[^_\n]+_(?!_)', 'Markdown emphasis'),
        (r'(?m)^\s*(?:[-+*]\s+|>\s*)', 'Markdown list or quote markers'),
        (r'<\s*/?\s*[A-Za-z][^>]*>', 'HTML tags'),
        (r'\\(?:\(|\)|\[|\])', r'\\(...\\) or \\[...\\] math'),
        (r'\\begin\s*\{(?:document|equation\*?|align\*?|displaymath)\}', 'document/display environments'),
        (r'\\[A-Za-z]+', 'LaTeX commands without $...$ delimiters'),
    ]
    for pattern, name in forbidden:
        if re.search(pattern, outside, re.IGNORECASE):
            raise ValueError(f"{label}: {name} are not allowed outside inline formulas")


def build(source):
    if not isinstance(source, dict) or not isinstance(source.get('title'), str) or not source['title'].strip():
        raise ValueError("source must be an object with a non-empty title")
    questions = source.get('questions')
    if not isinstance(questions, list) or not questions:
        raise ValueError("questions must be a non-empty array")
    seen = set()
    answers, mapping, sections = {}, [], [f"# {source['title'].strip()}", ""]
    for index, q in enumerate(questions, 1):
        if not isinstance(q, dict):
            raise ValueError(f"question entry {index} must be an object")
        number = q.get('number')
        if isinstance(number, bool) or not isinstance(number, (int, str)) or not str(number).strip():
            raise ValueError(f"question entry {index}: number must be a non-empty integer or string")
        key = str(number).strip()
        if key in seen:
            raise ValueError(f"duplicate question number: {key}")
        seen.add(key)
        title = q.get('title')
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"question {key}: title must be a non-empty string")
        answer, web_answer = q.get('answer'), q.get('web_answer')
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError(f"question {key}: answer must be non-empty report Markdown")
        validate_answer(web_answer, f"question {key} web_answer")
        page = q.get('page')
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError(f"question {key}: page must be a positive integer")
        delivery = q.get('delivery')
        if delivery not in ('text', 'photo'):
            raise ValueError(f"question {key}: delivery must be 'text' or 'photo'")
        if page != index:
            raise ValueError(f"question {key}: page must be {index} for one answer per page in report order")
        answers[key] = web_answer
        mapping.append({'number': key, 'page': page, 'delivery': delivery,
                        'photo': f"photos/page-{page:03d}.jpg" if delivery == 'photo' else None})
        sections.extend([f"## {key}. {title.strip()}", "", answer.rstrip(), ""])
    return '\n'.join(sections), answers, {'questions': mapping}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='UTF-8 JSON containing title and questions')
    parser.add_argument('--out-dir', type=Path, default=Path('.'), help='Output directory (default: current directory)')
    args = parser.parse_args()
    try:
        with args.source.open(encoding='utf-8') as stream:
            source = json.load(stream, object_pairs_hook=unique_object)
        report, answers, mapping = build(source)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        parser.exit(2, f"build_answers.py: {error}\n")
    # Validation and serialization are complete before any output is touched.
    try:
        out = args.out_dir
        (out / 'qa').mkdir(parents=True, exist_ok=True)
        (out / 'report.md').write_text(report, encoding='utf-8')
        (out / 'answers.json').write_text(json.dumps(answers, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (out / 'qa' / 'question-map.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    except OSError as error:
        parser.exit(2, f"build_answers.py: cannot write outputs: {error}\n")


if __name__ == '__main__':
    main()
