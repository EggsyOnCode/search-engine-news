import json
import hashlib

class MetaDataStore:
    def __init__(self):
        self.metadata_index = {}

    def store_metadata(self, title, source, date, url):
        # Calculate hash of the title
        doc_hash = hashlib.md5(title.encode()).hexdigest()

        # Store metadata against document hash
        self.metadata_index[doc_hash] = {
            'title': title,
            'source': source,
            'date': date,
            'url': url
        }

    def serialize_metadata(self, output_file):
        # Write the metadata index to a file
        with open(output_file, 'w', encoding='utf-8') as metadata_file:
            json.dump(self.metadata_index, metadata_file, ensure_ascii=False, indent=2)