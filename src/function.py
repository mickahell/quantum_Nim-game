"""Input controler to check the input from player."""
from qiskit import Aer, QuantumCircuit, execute


def control_input(options: int, input_ctl: int) -> bool:
    """Function to control input of user.
    Args:
        options: limit of input
        input_ctl: input of user
    Return: Bool
    """
    if input_ctl is not None:
        if isinstance(input_ctl, int):
            if 0 < input_ctl <= 3:
                return True
            else:
                print("Please give a number between 0 and {}.".format(options))
        else:
            if input_ctl in options:
                return True
            else:
                print("Please give a valid gate between {}".format(options))
    return False

def who_start(psi: int, backend_sim: Aer) -> int:
    """Function to check who start.
    Args:
        psi: angle for the qubit
        backend_sim: backend for running circuit
    Return: int
    """
    qc = QuantumCircuit(1, 1)

    qc.rx(math.pi * psi, 0)
    qc.measure(0, 0)

    job = execute(qc, backend_sim, shots=1, memory=True)
    result_job = job.result().get_memory()
    to_return = int(result_job[0], 2)

    return to_return
