from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository
from truckfactor.compute import main as compute_tf


class TruckFactor(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        for f in self._source_repository.src_paths:
            print(f)
        print(self._source_repository)
        tf, commit_sha, author_names = compute_tf(".", ouputkind=None)
        return tf


metric = TruckFactor()
metric.run()
