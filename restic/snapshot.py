import time
from datetime import datetime

class Snapshot(object):
    repo = None
    snapshot_id = None
    snapshot_time = None
    snapshot_host = None
    snapshot_tags = None
    snapshot_paths = None
    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def __str__(self):
        return f'{self.snapshot_id},{self.snapshot_time},{self.snapshot_host},{self.snapshot_tags},{self.snapshot_paths}'

    def is_valid(self):
        return self.repo is not None

    def check_valid(self):
        if not self.is_valid():
            raise RuntimeError('The snapshot is removed or updated, please get it from repo again')

    def set_attr(self, attr, value):
        if attr.strip() == 'ID':
            self.snapshot_id = value
        elif attr.strip() == 'Time':
            if type(value) == datetime:
                self.snapshot_time = value
            elif type(value) == str:
                self.snapshot_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        elif attr.strip() == 'Host':
            self.snapshot_host = value
        elif attr.strip() == 'Tags':
            self.snapshot_tags = value
        elif attr.strip() == 'Paths':
            self.snapshot_paths = value

    def get_id(self):
        return self.snapshot_id

    def get_time(self):
        return self.snapshot_time

    def get_host(self):
        return self.snapshot_host

    def get_tags(self):
        return self.snapshot_tags


    def get_paths(self):
        return self.snapshot_paths

    def add_tags(self, tags):
        self.check_valid()
        if type(tags) != list:
            raise ValueError('tags shall be type of list')
        self.repo.tag(add_tags=tags, remove_tags=None, set_tags=None, snapshot=self)

        # update id
        self.repo.update_snapshots_list()

    def add_tag(self, tag):
        self.check_valid()
        if type(tag) != str:
            raise ValueError('tag shall be type of str')
        self.repo.tag(add_tags=tag, remove_tags=None, set_tags=None, snapshot=self)

        # update id
        self.repo.update_snapshots_list()

    def remove_tags(self, tags):
        self.check_valid()
        
        if type(tags) != list:
            raise ValueError('tags shall be type of list')
        self.repo.tag(add_tags=None, remove_tags=tags, set_tags=None, snapshot=self)

        # update id
        self.repo.update_snapshots_list()

    def remove_tag(self, tag):
        self.check_valid()

        if type(tag) != str:
            raise ValueError('tag shall be type of str')
        self.repo.tag(add_tags=None, remove_tags=tag, set_tags=None, snapshot=self)

        # update id
        self.repo.update_snapshots_list()

    def set_tags(self, tags):
        self.check_valid()

        if type(tags) != list:
            raise ValueError('tags shall be type of list')
        self.repo.tag(add_tags=None, remove_tags=None, set_tags=tags, snapshot=self)

        # update id
        self.repo.update_snapshots_list()
    
    def set_tag(self, tag):
        self.check_valid()

        if type(tag) != str:
            raise ValueError('tag shall be type of str')
        self.repo.tag(add_tags=None, remove_tags=None, set_tags=tag, snapshot=self)

        # update id
        self.repo.update_snapshots_list()

    def restore(self, target):
        self.check_valid()

        self.repo.restore(target, self)

    