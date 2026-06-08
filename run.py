import argparse

from slotmachine.config import RUNCOUNT
from slotmachine.simulation import run_simulation


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo Slot Machine Simulator"
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=RUNCOUNT,
        help="Number of spins to simulate"
    )

    args = parser.parse_args()

    results = run_simulation(args.runs)

    print(f"Runs: {results['runs']:,}")
    print(f"Winnings: ${results['winnings']:.2f}")
    print(f"RTP: {results['rtp']:.2f}%")


if __name__ == "__main__":
    main()