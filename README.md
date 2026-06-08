# Slot Machine

(Alternatively named spreading infection)

A Monte Carlo slot machine simulator written in Python.

## Features

- 5 reel slot machine simulation
- Wild symbols
- Spread wild mechanics
- Bonus spins
- RTP calculation
- Configurable payouts
- Docker support

## Running

```bash
python run.py
```

```bash
python run.py --runs 1000000
```

## Docker

Build:

```bash
docker build -t slot-simulator .
```

Run:

```bash
docker run --rm slot-simulator
```

Custom run count:

```bash
docker run --rm slotmachine:optimized python run.py --runs 1000
```

## Testing

```bash
python -m pytest
```