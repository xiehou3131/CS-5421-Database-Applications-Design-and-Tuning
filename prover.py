class Prover:
    def __init__(self, R: list) -> None:
        self.attrs = R
        self.fds = []
        self.context = []
        self.status = {}
        self.goal = None
        self.errmsg = ""

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

        if self.exist(self.goal) != -1:
            return True
        
        print("Not finished:")
        print("    goal FD:", self.goal)
        print("    last FD:", self.fds[-1])
        return False

    def print_procedure(self) -> None:
        print(self.get_procedure())

    def get_procedure(self) -> str:
        ret = "# Arrtibutes:\n"
        ret += ','.join(sorted(self.attrs))

        ret += "\n\n# Goal:\n"
        ret += f"{','.join(sorted(self.goal[0]))} -> {','.join(sorted(self.goal[1]))}"
        ret += "\n\n# Proof.\n"
        for index in range(len(self.context)):
            ret += f" ({index + 1}) {self.context[index]['description']}\n"

        if self.finished():
            ret += "Q.E.D."
        return ret

    def print_fds(self) -> None:
        for fd in self.fds:
            print(sorted(fd))
    
    def exist(self, fd):
        lhs = sorted(set(fd[0]))
        rhs = sorted(set(fd[1]))

        for i in range(len(self.fds)):
            llhs = sorted(set(self.fds[i][0]))
            rrhs = sorted(set(self.fds[i][1]))
            if lhs == llhs and rhs == rrhs:
                return i + 1
        return -1
    
    def we_know_that(self, fd: list) -> bool:

        lhs = set(fd[0])
        rhs = set(fd[1])

        if not lhs.issubset(self.attrs):
            self.errmsg = f"The attribute in functional dependency {lhs} is not valid."
            return False

        if not rhs.issubset(self.attrs):
            self.errmsg = f"The attribute in functional dependency {rhs} is not valid."
            return False

        # loc = self.exist(fd)
        # if loc != -1:
        #     self.errmsg = f"We already know that {sorted(fd[0])} -> {sorted(fd[1])} at step ({loc})."
        #     return False

        ret = f"We know that {sorted(fd[0])} -> {sorted(fd[1])}."
        self.context.append({"fd": fd, "description": ret})
        self.fds.append(fd)
        self.errmsg = ""
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

        if not lhs.issubset(self.attrs):
            self.errmsg = (
                f"Reflexivity failed, the left-hand-side attribute {lhs} is not valid."
            )
            return False

        if not rhs.issubset(self.attrs):
            self.errmsg = (
                f"Reflexivity failed, the right-hand-side attribute {rhs} is not valid."
            )
            return False
        
        if rhs.issubset(lhs):
            ret = f"Therefore {sorted(lhs)} -> {sorted(rhs)} by Reflexivity."
            self.context.append(
                {
                    "fd": fd_dst,
                    "description": ret,
                }
            )
            self.fds.append(fd_dst)
            self.errmsg = ""
            return True

        self.errmsg = "Reflexivity failed, since the right-hand-side is not a subset of the left-hand-side."
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

            if not lhs1.issubset(self.attrs):
                self.errmsg = f"Augmentation failed, the left-hand-side attribute {lhs1} is not valid."
                return False

            if not rhs1.issubset(self.attrs):
                self.errmsg = f"Augmentation failed, the right-hand-side attribute {rhs1} is not valid."
                return False

            if not set(R).issubset(self.attrs):
                self.errmsg = (
                    f"Augmentation failed, the augmented attribute {R} is not valid."
                )
                return False
             
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
                self.errmsg = ""
                return True

            self.errmsg = f"Augmentation failed, '{','.join(sorted(fd_src[0]))}->{','.join(sorted(fd_src[1]))}' augment with '{','.join(sorted(R))}' does not equal to '{','.join(sorted(fd_dst[0]))}->{','.join(sorted(fd_dst[1]))}', please check the step ({stepA}) and the augmented attribute '{','.join(sorted(R))}'."
            return False
        except Exception as e:
            print(e)
            self.errmsg = "Augmentation failed, possibly the step number is not valid."
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

                if lhs_new == set(fd_dst[0]) and rhs_new == set(fd_dst[1]):

                    fd_new = [list(lhs_new), list(rhs_new)]
                    ret = f"Therefore {sorted(lhs_new)} -> {sorted(rhs_new)} by Transitivity of ({stepB}) and ({stepA})."
                    self.context.append(
                        {
                            "fd": fd_new,
                            "description": ret,
                        }
                    )
                    self.fds.append(fd_new)
                    self.errmsg = ""
                    return True

            fdB = self.context[stepA - 1]["fd"]
            fdA = self.context[stepB - 1]["fd"]
        self.errmsg = "Transitivity failed, please check the arguments."
        return False

    """
    Check Multi-valued Armstrong Axioms Transitivity
    Args:
        fd (list): The Multi-valued dependency result you want to check
        stepA (int): The step number in the prover's context
        stepB (int): The step number in the prover's context
    Returns:
    """
    def mv_transitivity(self, fd_dst, stepA: int, stepB: int) -> bool:
        # Therefore `fd` by Transitivity of `stepA` and `stepB`
        # Example:
        #   (3) {A, C} → {A, B, C}
        #   (4) {C} → {A, C}
        #
        #     Therefore {C} → {A, B, C} by Transitivity of (4) and (3).
        
        fdA = self.context[stepA - 1]["mvd"]
        fdB = self.context[stepB - 1]["mvd"]

        for _ in range(2):
            lhs1 = set(fdA[0])
            rhs1 = set(fdA[1])
            lhs2 = set(fdB[0])
            rhs2 = set(fdB[1])

            if rhs1 == lhs2:
                lhs_new = lhs1
                rhs_new = rhs2 - rhs1

                if lhs_new == set(fd_dst[0]) and rhs_new == set(fd_dst[1]):

                    mvd_new = [list(lhs_new), list(rhs_new)]
                    ret = f"Therefore {sorted(lhs_new)} ->> {sorted(rhs_new)} by Transitivity of ({stepB}) and ({stepA})."
                    self.context.append(
                        {
                            "mvd": mvd_new,
                            "description": ret,
                        }
                    )
                    self.fds.append(mvd_new)
                    self.errmsg = ""
                    return True

            fdB = self.context[stepA - 1]["fd"]
            fdA = self.context[stepB - 1]["fd"]
        self.errmsg = "Transitivity failed, please check the arguments."
        return False