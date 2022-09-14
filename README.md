# Aquis Exchange

### Content: (In logical order)
- [Main entry point](/project/__main__.py)
- [File Downloader](/project/file_downloader.py)
- [TSV Processor](/project/tsv_processor.py)

### Result => Generated TSV:
- [TSV](/generated_tsv/market_data.tsv)


### How to run?
Requirements: Python 3.9.5 (& pip 22.2.2)

```
$ pip install -r requirements.txt
```

```
$ python project
```

### How to run with docker:

```
$ docker build -t <project_name/aquis> .
```

```
$ docker run <project_name/aquis>
```

> Files will be stored inside the container by default.
> If you wish to copy them from the container to your host/local use docker cp.

```
$ docker cp <container_id>:<source> <destination>
```

>e.g. docker cp 60e3863f09d7:/app/downloads/ .