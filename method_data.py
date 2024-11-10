class MethodData:
    def __init__(self,
                 title,
                 stat,
                 stat_indv,
                 t,
                 e,
                 stat_indv_n,
                 post_proc = lambda x: x):
        self.title = title
        self.stat = stat
        self.stat_indv = stat_indv
        self.t = t
        self.e = e
        self.stat_indv_n = stat_indv_n
        self.post_proc = post_proc

class SelectedFileData:
    def __init__(self, e, t, similarity):
        self.e = e
        self.t = t
        self.similarity = similarity