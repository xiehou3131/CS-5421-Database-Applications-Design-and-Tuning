class Prover:
    def __init__(self, R: list) -> None:
        self.attrs = R
        self.fds = []
        self.context = []
        self.status = {}
        self.goal = None

    def set_goal(self, fd) -> bool:
        lhs = set(fd[0])
        rhs = set(fd[1])
        self.goal = [sorted(list(lhs)), sorted(list(rhs))]
        return True
    
    def finished(self) -> bool:
        if self.goal is None:
            raise Exception("No goal is set.")
        if len(self.fds) == 0:
            return False
        
        goal_lhs = set(self.goal[0])
        goal_rhs = set(self.goal[1])
        last_lhs = set(self.fds[-1][0])
        last_rhs = set(self.fds[-1][1])

        if goal_lhs == last_lhs and goal_rhs == last_rhs:
            return True
        print("Not finished:")
        print("    goal FD:", self.goal)
        print("    last FD:", self.fds[-1])
        return False

    def print_procedure(self) -> None:
        print(self.get_procedure())

    def get_procedure(self) -> str:
        ret = "Arrtibutes:\n"
        ret += str(sorted(self.attrs))

        ret += "\n\nGoal:\n"
        ret += str(self.goal)
        ret += "\n\nProof.\n"
        for index in range(len(self.context)):
            ret += f" ({index + 1}) {self.context[index]['description']}\n"

        if self.finished():
            ret += " Q.E.D."
        return ret

    def print_fds(self) -> None:
        for fd in self.fds:
            print(sorted(fd))

    def we_know_that(self, fd: list) -> bool:
        ret = f"We know that {sorted(fd[0])} -> {sorted(fd[1])}."
        self.context.append({"fd": fd, "description": ret})
        self.fds.append(fd)
        return True

    """
    Check Armstrong Axioms Reflexivity
    Args:
        fd (list): The functional dependency result you want to check
        stepA (int): The step number in the prover's context
    Returns:
    """

    def reflexivity(self, fd_dst, stepA: int = 0) -> str:
        # TODO: stepA is not used
        # Therefore `fd` by Reflexivity since `stepA`.
        # Example:
        #     (6) We know that {B,C} ⊂ {A,B,C}.
        #     (7) Therefore {A, B, C} → {A, B} by Reflexivity since (6).
        lhs = set(fd_dst[0])
        rhs = set(fd_dst[1])
        if rhs.issubset(lhs):
            ret = f"Therefore {sorted(lhs)} -> {sorted(rhs)} by Reflexivity."
            self.context.append(
                {
                    "fd": fd_dst,
                    "description": ret,
                }
            )
            self.fds.append(fd_dst)
            return True
        return False

    """
    Check Armstrong Axioms Augmentation
    Args:
        fd (list): The functional dependency result you want to check
        step (int): The step number in the prover's context
        R (list): Augment with [ A, B, C ... ]
    Returns:
    """

    def augmentation(self, fd_dst, stepA: int, R: list) -> bool:
        # Therefore `fd` by Augmentation of `stepA` with `R`
        # Example:
        #     Therefore {A, C} → {A, B, C} by Augmentation of (1) with {A, C}
        #     Therefore {C} → {A, C} by Augmentation of (2) with {C}

        #     We know that X→Y. (5)
        #     Therefore X → X ∪ Y by Augmentation of (5) with {X}.

        #     We know that X→Z. (6)
        #     Therefore X ∪ Y → Y ∪ Z by Augmentation of (6) with {Y}.

        try:
            fd_src = self.context[stepA - 1]["fd"]

            lhs1 = set(fd_dst[0])
            rhs1 = set(fd_dst[1])

            lhs2 = set(fd_src[0]).union(set(R))  # left-hand-side after augmentation
            rhs2 = set(fd_src[1]).union(set(R))  # right-hand-side after augmentation

            if lhs1 == lhs2 and rhs1 == rhs2:
                ret = f"Therefore {sorted(lhs1)} -> {sorted(rhs1)} by Augmentation of ({stepA}) with {R}."
                self.context.append(
                    {
                        "fd": fd_dst,
                        "description": ret,
                    }
                )
                self.fds.append(fd_dst)
                return True
        except Exception as e:
            print(e)
        return False

    """
    Check Armstrong Axioms Transitivity
    Args:
        fd (list): The functional dependency result you want to check
        stepA (int): The step number in the prover's context
        stepB (int): The step number in the prover's context
    Returns:
    """

    def transitivity(self, fd_dst, stepA: int, stepB: int) -> bool:
        # Therefore `fd` by Transitivity of `stepA` and `stepB`
        # Example:
        #   (3) {A, C} → {A, B, C}
        #   (4) {C} → {A, C}
        #
        #     Therefore {C} → {A, B, C} by Transitivity of (4) and (3).

        fdA = self.context[stepA - 1]["fd"]
        fdB = self.context[stepB - 1]["fd"]

        for _ in range(2):
            lhs1 = set(fdA[0])
            rhs1 = set(fdA[1])
            lhs2 = set(fdB[0])
            rhs2 = set(fdB[1])

            if rhs1.issubset(lhs2):
                lhs_new = lhs1
                rhs_new = rhs2
                fd_new = [list(lhs_new), list(rhs_new)]
                ret = f"Therefore {sorted(lhs_new)} -> {sorted(rhs_new)} by Transitivity of ({stepB}) and ({stepA})."
                self.context.append(
                    {
                        "fd": fd_new,
                        "description": ret,
                    }
                )
                self.fds.append(fd_new)
                return True

            fdB = self.context[stepA - 1]["fd"]
            fdA = self.context[stepB - 1]["fd"]
        return False
