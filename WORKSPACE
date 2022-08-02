load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "a30abdfc7126d497a7698c29c46ea9901c6392d6ed315171a6df5ce433aa4502",
    strip_prefix = "rules_python-0.6.0",
    url = "https://github.com/bazelbuild/rules_python/archive/0.6.0.tar.gz",
)

# This one is only needed if you're using the packaging rules.
load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "dev_requirements",
    requirements = "//py:requirements.txt",
)
