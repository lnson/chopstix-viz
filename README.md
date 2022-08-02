## Prerequisites

Install `bazel` and `graphviz`. On a Mac:

```shell
brew install bazel graphviz
```

## Generate state machine graphs

In the home folder of the project, run

```shell
bazel run visualizer:chopstix_visualizer -- \
    --num_fingers=4 \
    --output_file=`pwd`/visualizer/game-state-4.dot
```