import shutil

from dulwich import porcelain

# make sure we're starting fresh
shutil.rmtree("demo_repo", ignore_errors=True)

repo = porcelain.init("demo_repo")

# create an initial commit, with our content.
with open("demo_repo/a_file.txt", "wb") as f:
    f.write(b"Blobfish are people too\n")
porcelain.add(repo, "demo_repo/a_file.txt")  # note path!
porcelain.commit(repo, b"The beginning", author=b"meejah <meejah@meejah.ca>")

# make a single change
with open("demo_repo/a_file.txt", "wb") as f:
    f.write(b"Blobfish are fish, not people\n")
porcelain.add(repo, "demo_repo/a_file.txt")
porcelain.commit(
    repo, b"blobfish are aquatic animals",
    author=b"meejah <meejah@meejah.ca>",
)
