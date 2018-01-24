from time import time
import shutil

from dulwich.objects import Blob, Tree, Commit, parse_timezone
from dulwich.repo import Repo
from dulwich.walk import Walker

repo = Repo("demo_repo")
walker = Walker(repo.object_store, include=[repo.head()])
for item in walker:
    print("{}".format(item.commit.sha().hexdigest()))
    for change in item.changes():
        print("  {}: {}".format(change.type, change.new.path.decode('ascii')))

