# CDB - Disk based Log Structured Hash Table Store

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
[![build](https://github.com/avinassh/cdb/actions/workflows/build.yml/badge.svg)](https://github.com/avinassh/cdb/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/avinassh/cdb/branch/master/graph/badge.svg?token=9SA8Q4L7AZ)](https://codecov.io/gh/avinassh/cdb)
[![GitHub license](https://badgen.net/github/license/Naereen/Strapdown.js)](https://github.com/avinassh/cdb/blob/master/LICENSE)

![architecture](https://user-images.githubusercontent.com/640792/166490746-fb41709e-cdb5-4c9a-a58b-f4e6d530b5c7.png)

Forked from [this repo](https://github.com/avinassh/py-caskdb/tree/master).

CaskDB is a disk-based, embedded, persistent, key-value store based on the 
[Riak's bitcask paper](https://riak.com/assets/bitcask-intro.pdf), written in 
Python. It is more focused on the educational 
capabilities than using it in production. The file format is platform, machine, 
and programming language independent. Say, the database file created from Python
on macOS should be compatible with Rust on Windows.