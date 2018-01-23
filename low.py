from time import time
import shutil

from dulwich.objects import Blob, Tree, Commit, parse_timezone
from dulwich.repo import Repo

# make sure we're starting fresh
shutil.rmtree("demo_repo", ignore_errors=True)

# the "lowest level" object in Git is probably the "blob"; it is just
# some data.

blob = Blob.from_string(b"Blobfish are people too\n")
print("Created blob with hash: {}".format(blob.sha().hexdigest()))

# if we actually want to store the Blob somewhere, we need a Git
# database (which is the ".git/objects/*" directories and files in a
# repository)

repo = Repo.init("demo_repo", mkdir=True)
print("Repository: {}".format(repo))

# this git database is called the "object store"; dulwich has an
# abstraction of this
store = repo.object_store
print("Object store: {}".format(store))
store.add_object(blob)
print("Added one object")

# notes:
# - single object file in .git/objects now
# - "git cat-file -p <hash>": see our file!
# - file is compressed (hexdump -C .git/objects/*)

# now lets create a real "tree" object so we can give our Blob a
# filename

tree = Tree()
tree.add(b"a_file.txt", 0o100644, blob.id)
print("Tree: {}".format(tree.sha().hexdigest()))
# note: still not "in" the object repository
store.add_object(tree)

# From a user perpective, Trees live in Commit objects
commit = Commit()
commit.tree = tree
commit.author = commit.committer = b"meejah <meejah@meejah.ca>"
commit.commit_time = commit.author_time = int(time())  # seconds since epoch
commit.commit_timezone = commit.author_timezone = -7 * (60 * 60)  # seconds offset; MST
commit.encoding = b"utf8"
commit.message = b"The beginning"
# no commit.parent because this is the first Commit

# again, not in the object store yet
store.add_object(commit)

# nothing points at this Tree yet!
# ...so, we will add a "master" branch
repo.refs[b'refs/heads/master'] = commit.id
print("Head: {}".format(repo.head().decode('ascii')))


# next, create another commit, changing the contents of our file

b2 = Blob.from_string(b"Blobfish are fish, not people\n")
t2 = Tree()
t2.add(b"a_file.txt", 0o100644, b2.id)
c2 = Commit()
c2.tree = t2
c2.parents = [commit.id]  # note: parents, not parent!
c2.author = c2.committer = b"meejah <meejah@meejah.ca>"
c2.commit_time = c2.author_time = int(time())  # seconds since epoch
c2.commit_timezone = c2.author_timezone = -7 * (60 * 60)  # seconds offset; MST
c2.encoding = b"utf8"
c2.message = b"blobfish are aquatic animals"

print("  blob: {}".format(b2.sha().hexdigest()))
print("  tree: {}".format(t2.sha().hexdigest()))
print("commit: {}".format(c2.sha().hexdigest()))

store.add_object(b2)
store.add_object(t2)
store.add_object(c2)

# actually extend master branch
repo.refs[b'refs/heads/master'] = c2.id
print("Head now: {}".format(repo.refs[b'HEAD'].decode('ascii')))
