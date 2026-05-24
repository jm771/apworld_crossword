#!/usr/bin/env python3
"""
Test script for the .puz file parser.
"""

from puz_parser import parse_puz, Direction, ClueId


def test_parser():
    """Test the .puz parser with the sample file."""

    # Load the test file
    with open("./NY Times - 20230101 - In Play.puz", "rb") as f:
        data = f.read()

    # Parse the file
    clue_map, letter_list = parse_puz(data)

    print("=" * 70)
    print("PUZ PARSER TEST RESULTS")
    print("=" * 70)
    print()

    # Test 1: Data structure types
    print("TEST 1: Data Structure Types")
    print("-" * 70)
    print(f"clue_map type: {type(clue_map).__name__}")
    print(f"letter_list type: {type(letter_list).__name__}")
    assert isinstance(clue_map, dict), "clue_map should be a dict"
    assert isinstance(letter_list, list), "letter_list should be a list"
    print("✓ PASSED")
    print()

    # Test 2: ClueId and Direction enum
    print("TEST 2: ClueId and Direction Enum")
    print("-" * 70)
    print(f"Direction.ACROSS value: {Direction.ACROSS.value}")
    print(f"Direction.DOWN value: {Direction.DOWN.value}")

    sample_clue_id = ClueId(Direction.ACROSS, 1)
    print(f"Sample ClueId: {sample_clue_id}")
    print(f"  direction: {sample_clue_id.direction}")
    print(f"  number: {sample_clue_id.number}")

    # Test that ClueId can be used as dict key
    assert sample_clue_id in clue_map, "ClueId should work as dict key"
    print("✓ PASSED")
    print()

    # Test 3: Clue map contents
    print("TEST 3: Clue Map Contents")
    print("-" * 70)
    across_count = sum(1 for k in clue_map.keys() if k.direction == Direction.ACROSS)
    down_count = sum(1 for k in clue_map.keys() if k.direction == Direction.DOWN)

    print(f"Total clues: {len(clue_map)}")
    print(f"Across clues: {across_count}")
    print(f"Down clues: {down_count}")

    assert len(clue_map) > 0, "Should have parsed some clues"
    assert across_count > 0, "Should have across clues"
    assert down_count > 0, "Should have down clues"
    print("✓ PASSED")
    print()

    # Test 4: ClueInfo structure
    print("TEST 4: ClueInfo Structure")
    print("-" * 70)
    first_across = ClueId(Direction.ACROSS, 1)
    if first_across in clue_map:
        info = clue_map[first_across]
        print(f"1-Across:")
        print(f"  Answer: {info.answer}")
        print(f"  Clue: {info.clue[:60]}...")

        assert hasattr(info, 'clue'), "ClueInfo should have 'clue' attribute"
        assert hasattr(info, 'answer'), "ClueInfo should have 'answer' attribute"
        assert isinstance(info.clue, str), "clue should be a string"
        assert isinstance(info.answer, str), "answer should be a string"
    print("✓ PASSED")
    print()

    # Test 5: Letter list structure
    print("TEST 5: Letter List Structure")
    print("-" * 70)
    print(f"Total letters in grid: {len(letter_list)}")

    if len(letter_list) > 0:
        letter, assocs = letter_list[0]
        print(f"First letter: '{letter}'")
        print(f"  Type: {type(letter).__name__}")
        print(f"  Number of associations: {len(assocs)}")

        assert isinstance(letter, str), "Letter should be a string"
        assert isinstance(assocs, list), "Associations should be a list"

        if len(assocs) > 0:
            clue_id, pos = assocs[0]
            print(f"  First association:")
            print(f"    ClueId: {clue_id}")
            print(f"    Position: {pos}")

            assert isinstance(clue_id, ClueId), "Association should contain ClueId"
            assert isinstance(pos, int), "Position should be an integer"
    print("✓ PASSED")
    print()

    # Test 6: Letter associations are correct
    print("TEST 6: Letter Associations Correctness")
    print("-" * 70)

    # Check first letter
    letter, assocs = letter_list[0]
    print(f"First letter '{letter}' associations:")
    for clue_id, pos in assocs:
        info = clue_map[clue_id]
        expected_letter = info.answer[pos]
        print(f"  {clue_id} pos {pos}: answer='{info.answer}', letter at pos='{expected_letter}'")
        assert letter == expected_letter, f"Letter mismatch: expected '{expected_letter}', got '{letter}'"

    print("✓ PASSED")
    print()

    # Test 7: Verify position indices by reconstructing an answer
    print("TEST 7: Reconstruct Answer from Letter List")
    print("-" * 70)

    # Pick a clue to test
    test_clue = ClueId(Direction.ACROSS, 1)
    if test_clue in clue_map:
        original_answer = clue_map[test_clue].answer
        print(f"Testing clue: {test_clue}")
        print(f"Original answer: {original_answer}")

        # Collect all letters for this clue from letter_list
        positions_found = []
        for letter, assocs in letter_list:
            for clue_id, pos in assocs:
                if clue_id == test_clue:
                    positions_found.append((pos, letter))

        # Sort by position and reconstruct
        positions_found.sort()
        reconstructed = ''.join(letter for _, letter in positions_found)
        print(f"Reconstructed answer: {reconstructed}")

        assert reconstructed == original_answer, f"Reconstruction failed: {reconstructed} != {original_answer}"
    print("✓ PASSED")
    print()

    # Test 8: Sample of clues
    print("TEST 8: Sample Clues")
    print("-" * 70)

    print("Sample ACROSS clues:")
    across_clues = sorted([k for k in clue_map.keys() if k.direction == Direction.ACROSS],
                         key=lambda c: c.number)
    for clue_id in across_clues[:3]:
        info = clue_map[clue_id]
        print(f"  {clue_id.number}: {info.answer}")
        print(f"     {info.clue}")

    print()
    print("Sample DOWN clues:")
    down_clues = sorted([k for k in clue_map.keys() if k.direction == Direction.DOWN],
                        key=lambda c: c.number)
    for clue_id in down_clues[:3]:
        info = clue_map[clue_id]
        print(f"  {clue_id.number}: {info.answer}")
        print(f"     {info.clue}")

    print("✓ PASSED")
    print()

    # Test 9: Check for crossed vs uncrossed letters
    print("TEST 9: Crossed Letters")
    print("-" * 70)

    crossed_count = sum(1 for _, assocs in letter_list if len(assocs) == 2)
    uncrossed_count = sum(1 for _, assocs in letter_list if len(assocs) == 1)

    print(f"Crossed letters (2 associations): {crossed_count}")
    print(f"Uncrossed letters (1 association): {uncrossed_count}")
    print(f"Total: {crossed_count + uncrossed_count}")

    assert crossed_count + uncrossed_count == len(letter_list), "All letters should be accounted for"
    print("✓ PASSED")
    print()

    # Summary
    print("=" * 70)
    print("ALL TESTS PASSED!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  Total clues parsed: {len(clue_map)}")
    print(f"  Total letters in grid: {len(letter_list)}")
    print(f"  Across clues: {across_count}")
    print(f"  Down clues: {down_count}")
    print(f"  Crossed letters: {crossed_count}")
    print(f"  Uncrossed letters: {uncrossed_count}")


if __name__ == "__main__":
    test_parser()
