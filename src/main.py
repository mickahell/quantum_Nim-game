"""Main functions."""
from typing import Tuple

from qiskit import Aer, QuantumCircuit, QuantumRegister, execute
from src.function import control_input, who_start
from src import draw, ia


def battle(player1: list, backend_sim: Aer) -> Tuple:
    """Battle game.
    Args:
        player1: player
        backend_sim: backend for quantum
    Return: winner, looser
    """

    play = True

    computer = [False, True]

    begin = who_start(psi=0.5, backend_sim=backend_sim)
    print("A quantum process choose who starts... Human or Robot")
    if begin == 0:
        player1[0] = True
        print("Human starts")
    else:
        computer[0] = True
        print("Robot starts")

    while play:
        # Generation of the first circuit with 11 qubits
        stick = 11
        nb_qubit = stick
        drawing_add = ""
        draw.draw(stick, drawing_add)

        stick_qubit = QuantumRegister(nb_qubit, "stick")
        qc_board = QuantumCircuit(stick_qubit)

        # Game
        while stick > 0:
            player_name = player1[1]

            # Player choice
            if player1[0]:
                print(player_name, "- You take : ")
                control = False
                while not control:
                    nbstick = int(input())
                    control = control_input(stick, nbstick)
                for i in range(nbstick):
                    print(
                        player_name,
                        "- Which gate do you want to use on stick[",
                        i + 1,
                        "] ?",
                    )
                    control = False
                    while not control:
                        if stick - i == 1 and nb_qubit == 1:
                            gate = str(input("x : "))
                            control = control_input(["x"], gate)
                        elif stick - i == 1:
                            gate = str(input("x, cx : "))
                            control = control_input(["x", "cx"], gate)
                        elif stick - i == nb_qubit:
                            gate = str(input("h, x : "))
                            control = control_input(["x", "h"], gate)
                        elif stick - i > 1:
                            gate = str(input("h, x, cx : "))
                            control = control_input(["x", "h", "cx"], gate)

                    if gate == "h":
                        qc_board.h(stick - (1 + i))
                        drawing_add = "/ " + drawing_add
                    if gate == "x":
                        qc_board.x(stick - (1 + i))
                        drawing_add = "x " + drawing_add
                    if gate == "cx":
                        qc_board.cx(stick - i, stick - (1 + i))
                        drawing_add = "¬ " + drawing_add

            # Computer choice
            if computer[0]:
                print("The robot is thinking ...")
                if stick == 1 and nb_qubit == 1:
                    qc_board.x(stick - 1)
                    drawing_add = "x " + drawing_add
                    nbstick = 1
                else:
                    past = drawing_add.split(" ")
                    result_analyse = ia.quantum_ia(stick, past, backend_sim)
                    for i, gate in enumerate(result_analyse):
                        if gate == "x":
                            qc_board.x(stick - (1 + i))
                            drawing_add = "x " + drawing_add
                        if gate == "sup":
                            qc_board.h(stick - (1 + i))
                            drawing_add = "/ " + drawing_add
                        if gate == "intric":
                            qc_board.cx(stick - i, stick - (1 + i))
                            drawing_add = "¬ " + drawing_add

                    nbstick = len(result_analyse)

            stick -= nbstick

            # Check if board is clean
            if stick < 1:
                # Run circuit
                qc_board.measure_all()
                print(qc_board.draw())
                job = execute(qc_board, backend_sim, shots=1, memory=True)
                result_memory = job.result().get_memory()
                result = result_memory[0]
                for i, _ in enumerate(result):
                    if result[i] == "0":
                        stick += 1
                print("stick left : ", stick)

                # Check circuit result
                if stick < 1:
                    if computer[0]:
                        print(
                            "\n\n##################\n  Player 1 win !\n##################"
                        )
                        return "human", "robot"
                    if computer[0] is False:
                        print(
                            "\n\n##################\n  Machine win !\n##################"
                        )
                        return "robot", "human"
                else:
                    # Generation of new circuit with qubits left
                    nb_qubit = stick
                    drawing_add = ""
                    stick_qubit = QuantumRegister(nb_qubit, "stick")
                    qc_board = QuantumCircuit(stick_qubit)

            # Inverse turn
            if stick > 0:
                draw.draw(stick, drawing_add)
                player1[0] = not player1[0]
                if computer[1]:
                    computer[0] = not computer[0]
