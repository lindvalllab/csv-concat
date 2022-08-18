import filecmp
import os

from concatenator import Concatenator

file_prefix = os.path.join(
    os.path.dirname(__file__),
    "files/"
)


def test_concatenate_all_columns_no_arg() -> None:
    concatenator = Concatenator([
        os.path.join(file_prefix, "1.csv"),
        os.path.join(file_prefix, "2.csv"),
        os.path.join(file_prefix, "3.csv")
    ])

    with open(os.path.join(file_prefix, "test_all_cols_1.csv"), 'w') as out_file:
        concatenator.write_file(out_file)

    assert filecmp.cmp(
        os.path.join(file_prefix, "test_all_cols_1.csv"),
        os.path.join(file_prefix, "1_2_3_all_joined.csv")
    )


def test_concatenate_all_columns_none_arg() -> None:
    concatenator = Concatenator([
        os.path.join(file_prefix, "1.csv"),
        os.path.join(file_prefix, "2.csv"),
        os.path.join(file_prefix, "3.csv")
    ])

    with open(os.path.join(file_prefix, "test_all_cols_2.csv"), 'w') as out_file:
        concatenator.write_file(out_file, None)

    assert filecmp.cmp(
        os.path.join(file_prefix, "test_all_cols_2.csv"),
        os.path.join(file_prefix, "1_2_3_all_joined.csv")
    )


def test_concatenate_all_columns_explicitly() -> None:
    concatenator = Concatenator([
        os.path.join(file_prefix, "1.csv"),
        os.path.join(file_prefix, "2.csv"),
        os.path.join(file_prefix, "3.csv")
    ])

    with open(os.path.join(file_prefix, "test_all_cols_3.csv"), 'w') as out_file:
        concatenator.write_file(out_file, [0, 1, 2, 3, 4])

    assert filecmp.cmp(
        os.path.join(file_prefix, "test_all_cols_3.csv"),
        os.path.join(file_prefix, "1_2_3_all_joined.csv")
    )


def test_concatenate_even_columns() -> None:
    concatenator = Concatenator([
        os.path.join(file_prefix, "1.csv"),
        os.path.join(file_prefix, "2.csv"),
        os.path.join(file_prefix, "3.csv"),
    ])

    with open(os.path.join(file_prefix, "test_even_cols.csv"), 'w') as out_file:
        concatenator.write_file(out_file, [0, 2, 4])

    assert filecmp.cmp(
        os.path.join(file_prefix, "test_even_cols.csv"),
        os.path.join(file_prefix, "1_2_3_even_cols.csv")
    )


def test_concatenate_odd_columns() -> None:
    concatenator = Concatenator([
        os.path.join(file_prefix, "1.csv"),
        os.path.join(file_prefix, "2.csv"),
        os.path.join(file_prefix, "3.csv"),
    ])

    with open(os.path.join(file_prefix, "test_odd_cols.csv"), 'w') as out_file:
        concatenator.write_file(out_file, [1, 3])

    assert filecmp.cmp(
        os.path.join(file_prefix, "test_odd_cols.csv"),
        os.path.join(file_prefix, "1_2_3_odd_cols.csv")
    )
