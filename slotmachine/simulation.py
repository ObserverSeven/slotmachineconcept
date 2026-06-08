from slotmachine.spreadinginfection import SlotSimulator

def run_simulation(runs):
    machine = SlotSimulator()

    for _ in range(runs):
        machine.total_winnings -= 1
        machine.spin()

    rtp = (machine.total_winnings / runs) * 100

    return {
        "runs": runs,
        "winnings": machine.total_winnings,
        "rtp": rtp
    }