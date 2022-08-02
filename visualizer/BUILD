load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@dev_requirements//:requirements.bzl", "requirement")

py_binary(
    name = "chopstix_visualizer",
    srcs = [
        "chopstix_visualizer.py",
    ],
    deps = [
        requirement("absl-py"),
        requirement("graphviz"),
    ],
)
