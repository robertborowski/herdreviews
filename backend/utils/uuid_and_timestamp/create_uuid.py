# -------------------------------------------------------------- Imports
import uuid

# -------------------------------------------------------------- Main
def create_uuid_function(table_prefix):
  return table_prefix + str(uuid.uuid4())