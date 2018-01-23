from time import time
import shutil

from dulwich.objects import Blob, Tree, Commit, parse_timezone
from dulwich.repo import Repo

# make sure we're starting fresh
shutil.rmtree("demo_repo", ignore_errors=True)

repo = Repo.init("demo_repo", mkdir=True)
print("Repository: {}".format(repo))

# create an initial commit, with our content.
with open("demo_repo/a_file.txt", "wb") as f:
    f.write(b"Blobfish are people too\n")
repo.stage([b"a_file.txt"])
repo.do_commit(
    b"The beginning",
    committer=b"meejah <meejah@meejah.ca>",
)

# make a single change
with open("demo_repo/a_file.txt", "wb") as f:
    f.write(b"Blobfish are fish, not people\n")
repo.stage([b"a_file.txt"])
repo.do_commit(
    b"blobfish are aquatic animals",
    committer=b"meejah <meejah@meejah.ca>",
)

