

class Snapshot(object):
    snapshot_id = None
    snapshot_time = None
    snapshot_host = None
    snapshot_tags = None
    snapshot_paths = None
    def __init__(self, snapshot_id=None, snapshot_time=None, snapshot_host=None, snapshot_tags=None, snapshot_paths=None):
        super().__init__()

        self.snapshot_id = snapshot_id
        self.snapshot_time = snapshot_time
        self.snapshot_host = snapshot_host
        self.snapshot_tags = snapshot_tags
        self.snapshot_paths = snapshot_paths

    def set_attr(self, attr, value):
        if attr.strip() == 'ID':
            self.snapshot_id = value
        elif attr.strip() == 'Time':
            self.snapshot_time = value
        elif attr.strip() == 'Host':
            self.snapshot_host = value
        elif attr.strip() == 'Tags':
            self.snapshot_tags = value
        elif attr.strip() == 'Paths':
            self.snapshot_paths = value

    