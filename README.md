# Poetry and Python Benchmark

This repository serves to benchmark the performance of [Poetry](https://python-poetry.org/)
when using different version.

The idea for this release came after the release of the new [Python 3.13](https://docs.python.org/3/whatsnew/3.13.html)
with the option to disable the [GIL](https://wiki.python.org/moin/GlobalInterpreterLock).

This repository is heavily inspired by the [python-package-manager-shootout](https://github.com/lincolnloop/python-package-manager-shootout) repository.

Similarly to that repository, we use a list of packages from a fixed version of [Sentry's `requirements.txt file`](https://github.com/getsentry/sentry/blob/da11f63098ef5c661e879effb8688178bb5eccee/requirements-base.txt) which was chosen arbitrarily as a non-trivial real-world example.
We however use a newer version to avoid any issues during package installation with newer Python versions.

Unlike in [python-package-manager-shootout](https://lincolnloop.github.io/python-package-manager-shootout/),
we use a newer version of Sentry's requirements to avoid any issues with the newer Python version. Additionally, we use [hyperfine](https://github.com/sharkdp/hyperfine) to time the execution of each command and to generate results and plots

