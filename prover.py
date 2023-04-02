class Prover:

    def __init__(self, R: list) -> None:
        self.fds = []
        self.context = []
        self.steps = []
        self.status = {}
        self.goal = None

    def set_goal(self, fd) -> None:
        lhs = set(fd[0])
        rhs = set(fd[1])
        self.goal = [sorted(list(lhs)), sorted(list(rhs))]

    def finished(self) -> bool:
        if self.goal is None:
            raise Exception("No goal is set.")
        
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
    
    def print_context(self) -> None:
        print("\nProof.")
        for index in range(len(self.context)):
            print(f" ({index + 1}) {self.context[index]['description']}")

        print("Q.E.D.\n")

    def print_fds(self) -> None:
        for fd in self.fds:
            print(sorted(fd))

    def we_know_that(self, fd: list) -> None:
        self.fds.append(fd)
        self.context.append(
            {"fd": fd, "description": f"We know that {sorted(fd[0])} -> {sorted(fd[1])}."}
        )

    """
    Check Armstrong Axioms Reflexivity
    Args:
        fd (list): The functional dependency result you want to check
        stepA (int): The step number in the prover's context
    Returns:
    """

    def reflexivity(self, fd_dst, stepA: int) -> bool:
        # TODO: stepA is not used
        # Therefore `fd` by Reflexivity since `stepA`.
        # Example:
        #     (6) We know that {B,C} ⊂ {A,B,C}.
        #     (7) Therefore {A, B, C} → {A, B} by Reflexivity since (6).
        lhs = set(fd_dst[0])
        rhs = set(fd_dst[1])
        if rhs.issubset(lhs):
            self.context.append(
                {
                    "fd": fd_dst,
                    "description": f"Therefore {lhs} -> {rhs} by Reflexivity since ({stepA}).",
                }
            )
            self.fds.append(fd_dst)
            return True
        raise Exception("Reflexivity failed.")

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

        fd_src = self.context[stepA - 1]["fd"]

        lhs1 = set(fd_dst[0])
        rhs1 = set(fd_dst[1])

        lhs2 = set(fd_src[0]).union(set(R)) # left-hand-side after augmentation
        rhs2 = set(fd_src[1]).union(set(R)) # right-hand-side after augmentation

        if lhs1 == lhs2 and rhs1 == rhs2:
            self.context.append(
                {
                    "fd": fd_dst,
                    "description": f"Therefore {sorted(lhs1)} -> {sorted(rhs1)} by Augmentation of ({stepA}) with {R}.",
                }
            )
            self.fds.append(fd_dst)
            return True
        raise Exception("Augmentation failed")

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
                self.context.append(
                    {
                        "fd": fd_new,
                        "description": f"Therefore {sorted(lhs_new)} -> {sorted(rhs_new)} by Transitivity of ({stepB}) and ({stepA}).",
                    }
                )
                self.fds.append(fd_new)
                return True

            fdB = self.context[stepA - 1]["fd"]
            fdA = self.context[stepB - 1]["fd"]


        raise Exception("Transitivity failed")
