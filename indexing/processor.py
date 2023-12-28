import os
import time
from forward_index import ForwardIndex
from indexing.reversed_index import ReversedIndex
from constants import (
    xen_deserialize_reverse_index
)

forwardIndex = ForwardIndex()
forwardIndex.genIndex()
# forwardIndex.serialize_index()
# forwardIndex.deserialize_index_from_json("./data/forward_index/new_index.json")
# reverseIndex = ReversedIndex("search", 2500)
# reverseIndex.genIndex(forwardIndex)
# reverseIndex.serialize_index("./data/reversed_index")
# reverseIndex.serialize_lexicon("./data/lexicon")


