
# Problem 1 Parsing Solution

Generate fixed-width file:

Used offsets specified in the spec file to determine field widths.
Pad fields with whitespace if content is shorter than specified width.


Parse fixed-width file:

Implemented a parser to read the fixed-width file.
Convert to a delimited format (e.g. CSV).
Trim whitespace from field values during conversion.

### Run main script
You can run the script with or without arguments. By default, it will generate 5 records if no arguments are provided.

#### With `--records` argument (e.g., 2000 records):
```bash
python main.py --records 20
```

### Run test script
```bash
python -m unittest discover -s .
```

## Running Through Docker

### Build Docker image
Make sure you are in the correct directory where the Dockerfile is located. so your terminal m
```bash
docker build -t problem1 .
```

### Run main script in Docker
You can also specify the number of records in the Docker run command.


#### With `--records` argument (e.g., 2000 records):
```bash
docker run -v $PWD/output:/app/output problem1 python main.py --records 20
```

### Run test script in Docker
```bash
docker run problem1 python -m unittest discover -s .
```
