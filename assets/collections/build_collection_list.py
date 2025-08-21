from pathlib import Path

SOKOBAN_COLLECTION_SUFFIX = ".slc"
COLLECTION_LIST_NAME = "collection_list.txt"

parent_path = Path(__file__).parent
collection_list_path = parent_path / COLLECTION_LIST_NAME

collection_list = [
    item.name
    for item in parent_path.iterdir()
    if item.suffix == SOKOBAN_COLLECTION_SUFFIX
]

# collection_list.sort()

collection_list_str = "\n".join(collection_list)

collection_list_path.write_text(collection_list_str)
