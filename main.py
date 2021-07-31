import random_improver
import random_tree_searcher

def main():
    """
    Inputs are the following two variables
    In "participants" you should put a list of attending people
    In "rounds_template" you should put a list of strings, which have the same number of "_" characters
    as the number of participants. After that put "|" characters in between, to create groups. See the below example:
    :return:
    """
    participants = "James,Robert,John,Michael,William,David,Richard,Joseph,Thomas,Charles".split(
        ",")
    rounds_template = [
        "____|____|__",  # 2 groups of 4 and one group of 2 people
        "____|____|__",
        "____|____|__",
        "___|____|___"  # 2 groups of 3 and one group of 4 people
    ]
    for i in range(len(rounds_template)):
        if len(participants) != sum(c == "_" for c in rounds_template[i]):
            raise Exception(f"In round {i} the number of participants doesn't "
                            f"match the number of _ in the round template")
    random_improver.random_improver(participants, rounds_template)
    # you can use the following function instead
    # (takes more time and sometimes produces better results)
    # random_tree_searcher.random_tree_searcher(participants, rounds_template)


if __name__ == '__main__':
    main()
