import json
import os

class FileRegistry:
    def __init__(self, registry_path='registry.json'):
        self.registry_path = registry_path
        self.registry = self.load_registry()

# load existing registry
    def load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {}
    
# save registry
    def save_registry(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=4)

# get files from drive (new or updated)
    def get_new_or_updated_files(self, drive_files):
        new_or_updated_files = []
    
        for file in drive_files:
            file_id = file['id']
            modified_time = file['modifiedTime']
        
            if (file_id not in self.registry) or (self.registry[file_id] != modified_time):
                new_or_updated_files.append(file)
                
        return new_or_updated_files
    
# update registry after processing files
    def update(self, file_id, modified_time):
        self.registry[file_id] = modified_time
        self.save_registry()



